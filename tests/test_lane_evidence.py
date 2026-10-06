"""Static guidance and an independent checker for normalized live host evidence.

This module does not route a prompt or simulate a host. The optional CLI checks
actual observations normalized by a reviewer from saved replies and tool traces.
Withhold fixture `expected` from hosts. Supply `source_reads` from actual tool
receipts, not a host's assertion. Acceptance covers these cases only, not general
model adherence. Unit tests below exercise checker behavior with concrete inputs.
"""
import argparse
import copy
import json
from pathlib import Path
import sys
import unittest

from test_wp2_contract import MODE, section, steps

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/rc2-lane-evidence.json'


def observation_errors(case, observation, source_reads=()):
    """Compare a normalized reply with independently authored expected evidence."""
    errors = []
    if not isinstance(source_reads, (list, tuple)) or any(not isinstance(path, str) for path in source_reads):
        errors.append('source reads must be a list of independently recorded paths')
        source_reads = ()
    for field, expected in case['expected'].items():
        if field not in observation or observation[field] != expected:
            errors.append(f'{field}: expected {expected!r}, got {observation.get(field)!r}')
    basis = observation.get('language_basis')
    evidence = observation.get('language_evidence')
    if basis == 'unresolved':
        if 'language_evidence' not in observation or evidence is not None:
            errors.append('unresolved language must have null evidence')
    elif basis in ('request', 'source'):
        if not isinstance(evidence, dict):
            errors.append('language evidence missing')
        else:
            reference, quote = evidence.get('reference'), evidence.get('quote')
            content = case['prompt'] if basis == 'request' and reference == 'request' else None
            if basis == 'source' and isinstance(reference, str) and reference in case['files'] and reference in source_reads:
                content = case['files'][reference]
            if content is None or not isinstance(quote, str) or not quote.strip() or quote not in content:
                errors.append('language citation absent from request or independently recorded source read')
            # A DSL declaration cannot establish app implementation language.
            if basis == 'source' and isinstance(reference, str) and reference.endswith('.gradle.kts'):
                errors.append('build-script DSL is not app-language evidence')
            language = observation.get('implementation_language')
            if basis == 'request' and (not isinstance(language, str) or not isinstance(quote, str) or language not in quote):
                errors.append('request citation must explicitly name the claimed language')
    else:
        errors.append('invalid language basis')
    return errors


def guidance_errors(mode, lanes):
    """Check Markdown relationships/gates only; never infer model compliance."""
    errors = []
    numbered = dict(steps(mode))
    first = numbered.get('1', '')
    if 'references/mobile-lanes.md#lane-evidence' not in first or 'Complete this step' not in first:
        errors.append('mode evidence completion gate')
    preview = numbered.get('3', '')
    if 'lane evidence record' not in preview or 'unresolved fields' not in preview:
        errors.append('preview evidence output')
    record = section(lanes, 'Lane evidence')
    dimensions = ('Platform', 'Implementation language', 'Framework or shared ownership', 'Affected target')
    for dimension in dimensions:
        if not any(line.startswith('| ' + dimension + ' |') for line in record.splitlines()):
            errors.append('missing evidence dimension: ' + dimension)
    guards = ('request-derived', 'before execution', 'build.gradle.kts',
              'build-script DSL', 'Android, Gradle or Pixel', 'iOS or Xcode',
              'source evidence', 'language-specific lane or test runner',
              'build-doctor', 'Scoped source evidence takes precedence')
    for guard in guards:
        if guard not in record:
            errors.append('missing lane guard: ' + guard)
    # Relate authored native-language examples to their own explicit prompt,
    # instead of pinning an entire prompt string.
    for row in section(mode, 'Routing examples').splitlines():
        cells = [cell.strip() for cell in row.split('|')[1:-1]]
        if len(cells) != 3:
            continue
        request, _, domain = cells
        if 'Swift/iOS' in domain and 'Swift' not in request:
            errors.append('Swift example lacks request language evidence')
        if 'Kotlin/Android' in domain and 'Kotlin' not in request:
            errors.append('Kotlin example lacks request language evidence')
        if 'KMP shared logic' in domain and 'KMP' not in request:
            errors.append('KMP example lacks request ownership evidence')
    return errors


def check_observations(records):
    cases = {case['id']: case for case in json.loads(FIXTURE.read_text())['cases']}
    results = []
    for record in records:
        if not isinstance(record, dict):
            results.append({'case_id': None, 'errors': ['invalid observation record']})
            continue
        case_id = record.get('case_id')
        if case_id not in cases:
            errors = ['unknown fixture case']
        elif not isinstance(record.get('observation'), dict):
            errors = ['missing normalized observation']
        else:
            errors = observation_errors(cases[case_id], record['observation'], record.get('source_reads', []))
        results.append({'case_id': case_id, 'errors': errors})
    return results


class LaneEvidence(unittest.TestCase):
    def setUp(self):
        self.cases = {case['id']: case for case in json.loads(FIXTURE.read_text())['cases']}
        self.mode = (ROOT / MODE / 'SKILL.md').read_text()
        self.lanes = (ROOT / MODE / 'references/mobile-lanes.md').read_text()

    def observation(self, case_id, reference=None, quote=None):
        # Construct checker inputs, not fabricated host results.
        reply = dict(self.cases[case_id]['expected'])
        reply['language_evidence'] = None if reference is None else {'reference': reference, 'quote': quote}
        return reply

    def test_static_guidance_has_complete_evidence_gate(self):
        self.assertEqual(guidance_errors(self.mode, self.lanes), [])

    def test_gate_and_each_dimension_mutations_rejected(self):
        self.assertEqual(guidance_errors(self.mode, self.lanes), [])
        mutated = self.mode.replace('references/mobile-lanes.md#lane-evidence', 'references/mobile-lanes.md')
        self.assertIn('mode evidence completion gate', guidance_errors(mutated, self.lanes))
        mutated = self.mode.replace('lane evidence record', 'domain')
        self.assertIn('preview evidence output', guidance_errors(mutated, self.lanes))
        for dimension in ('Platform', 'Implementation language', 'Framework or shared ownership', 'Affected target'):
            with self.subTest(dimension=dimension):
                mutated = self.lanes.replace('| ' + dimension + ' |', '| omitted |')
                self.assertIn('missing evidence dimension: ' + dimension, guidance_errors(self.mode, mutated))

    def test_example_labels_need_evidence_in_their_own_request(self):
        self.assertEqual(guidance_errors(self.mode, self.lanes), [])
        for phrase, replacement, error in [
                ('the Swift article list', 'the article list', 'Swift example lacks request language evidence'),
                ('Kotlin Android topic screen', 'topic screen', 'Kotlin example lacks request language evidence'),
                ('KMP shared code', 'shared code', 'KMP example lacks request ownership evidence')]:
            with self.subTest(example=phrase):
                self.assertIn(error, guidance_errors(self.mode.replace(phrase, replacement), self.lanes))

    def test_platform_only_unresolved_accepted_and_guessed_language_rejected(self):
        for case_id, guessed in [('android-gradle-only', 'Kotlin'), ('ios-xcode-only', 'Swift')]:
            with self.subTest(case=case_id):
                observation = self.observation(case_id)
                self.assertEqual(observation_errors(self.cases[case_id], observation), [])
                observation['implementation_language'] = guessed
                observation['language_basis'] = 'request'
                observation['language_evidence'] = {'reference': 'request', 'quote': self.cases[case_id]['prompt']}
                errors = observation_errors(self.cases[case_id], observation)
                self.assertTrue(any(error.startswith('implementation_language:') for error in errors))
                self.assertIn('request citation must explicitly name the claimed language', errors)

    def test_request_language_accepted_but_not_repository_verified(self):
        case_id = 'explicit-kotlin-request'
        observation = self.observation(case_id, 'request', 'Kotlin Android')
        self.assertEqual(observation_errors(self.cases[case_id], observation), [])
        observation['language_basis'] = 'source'
        self.assertIn('language_basis: expected \'request\', got \'source\'',
                      observation_errors(self.cases[case_id], observation))

    def test_actual_source_read_citation_required_for_positive_controls(self):
        for case_id in ('scoped-kotlin-source', 'scoped-swift-source', 'gradle-kotlin-dsl-java'):
            case = self.cases[case_id]
            reference = next(path for path in case['files'] if not path.endswith('.gradle.kts'))
            observation = self.observation(case_id, reference, case['files'][reference].strip())
            with self.subTest(case=case_id):
                self.assertEqual(observation_errors(case, observation, [reference]), [])
                self.assertIn('language citation absent from request or independently recorded source read',
                              observation_errors(case, observation))
                observation['language_evidence']['quote'] = 'invented source text'
                self.assertIn('language citation absent from request or independently recorded source read',
                              observation_errors(case, observation, [reference]))

    def test_kotlin_DSL_does_not_override_actual_Java_source(self):
        case_id = 'gradle-kotlin-dsl-java'
        case = self.cases[case_id]
        source = 'app/src/main/java/example/MainActivity.java'
        observation = self.observation(case_id, source, 'public class MainActivity')
        self.assertEqual(observation_errors(case, observation, [source]), [])
        observation.update(implementation_language='Kotlin', lane='Kotlin/Android')
        observation['language_evidence'] = {'reference': 'build.gradle.kts', 'quote': 'plugins { id("com.android.application") }'}
        errors = observation_errors(case, observation, ['build.gradle.kts', source])
        self.assertIn('build-script DSL is not app-language evidence', errors)
        self.assertTrue(any(error.startswith('implementation_language:') for error in errors))

    def test_known_platform_does_not_fill_ownership_target_or_runner(self):
        observation = self.observation('android-gradle-only')
        self.assertEqual(observation_errors(self.cases['android-gradle-only'], observation), [])
        for field, guess in [('framework_or_shared_ownership', 'Jetpack Compose'),
                             ('affected_target', 'app:demoDebug'), ('lane', 'Kotlin/Android')]:
            mutated = copy.deepcopy(observation)
            mutated[field] = guess
            self.assertTrue(any(error.startswith(field + ':') for error in
                                observation_errors(self.cases['android-gradle-only'], mutated)))

    def test_reading_build_file_does_not_substitute_source_receipt(self):
        case = self.cases['gradle-kotlin-dsl-java']
        observation = self.observation(case['id'], 'app/src/main/java/example/MainActivity.java', 'public class MainActivity')
        self.assertIn('language citation absent from request or independently recorded source read',
                      observation_errors(case, observation, ['build.gradle.kts']))

    def test_malformed_language_citations_are_rejected(self):
        case = self.cases['explicit-kotlin-request']
        observation = self.observation(case['id'], 'request', 42)
        self.assertIn('request citation must explicitly name the claimed language',
                      observation_errors(case, observation))
        case = self.cases['scoped-kotlin-source']
        observation = self.observation(case['id'], ['not-a-path'], 'class Label')
        self.assertIn('language citation absent from request or independently recorded source read',
                      observation_errors(case, observation))

    def test_self_report_is_not_a_source_read_receipt(self):
        case = self.cases['scoped-kotlin-source']
        reference = 'app/src/main/kotlin/example/Label.kt'
        observation = self.observation(case['id'], reference, 'class Label')
        self.assertIn('source reads must be a list of independently recorded paths',
                      observation_errors(case, observation, reference))
        self.assertIn('language citation absent from request or independently recorded source read',
                      observation_errors(case, observation, reference))
        self.assertEqual(observation_errors(case, observation, [reference]), [])

    def test_checker_unknown_case_and_missing_fields_rejected(self):
        self.assertEqual(check_observations([{'case_id': 'missing', 'observation': {}}]),
                         [{'case_id': 'missing', 'errors': ['unknown fixture case']}])
        observation = self.observation('android-gradle-only')
        del observation['affected_target']
        self.assertIn('affected_target: expected None, got None',
                      check_observations([{'case_id': 'android-gradle-only', 'observation': observation}])[0]['errors'])


if __name__ == '__main__':
    if '--check-observations' in sys.argv:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--check-observations', type=Path, required=True)
        records = json.loads(parser.parse_args().check_observations.read_text())
        results = check_observations(records)
        print(json.dumps(results, indent=2))
        sys.exit(1 if not results or any(result['errors'] for result in results) else 0)
    unittest.main()
