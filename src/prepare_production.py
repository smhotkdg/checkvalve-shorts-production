"""Prepare a connector-led Higgsfield + Typecast run without submitting jobs."""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def prepare(output_dir):
    config = json.loads((ROOT / 'config/higgsfield-typecast.json').read_text(encoding='utf-8'))
    script = json.loads((ROOT / 'src/checkvalve/script.json').read_text(encoding='utf-8'))
    narration = ' '.join(beat['phrase'] for beat in script['beats'])
    shared = ('Original stylized engineering cutaway explainer. Consistent dark navy background, '
              'cyan water, gold spring, ivory solid poppet and coral closed-state accent. '
              'No people, no logos, no text, no speech. Leave top title area and bottom caption area clear. '
              'Keep the same housing, fixed annular seat, moving solid poppet, axial stem, spring and retainer. '
              'Water bypasses the solid poppet through the surrounding open gap; it never crosses solid parts.')
    image_prompts = [
        'A staged cutaway engineering explainer scene showing a spring check valve in a pipe. Establish the visual style and clear layout.',
        'Detailed mechanism reference in the same staged environment: closed and open configurations of one identical spring check valve.',
        'Matching pipe-and-pump environment reference with ample central room for the approved valve mechanism.'
    ]
    scenes = [
        'Problem: a pump stops; suggest water attempting to return, then introduce the closed check valve.',
        'Structure: inspect the fixed seat, solid moving poppet, spring and fixed retainer in clear cutaway detail.',
        'Opening: forward differential pressure moves the poppet right and compresses the spring; cyan particles bypass the solid poppet.',
        'Closing: pressure difference decreases, spring returns the poppet to the seat; reverse pressure helps hold it closed.',
        'Operating condition: show insufficient then sufficient differential pressure and finish with a clear open/closed recap.'
    ]
    images = [{'index': i+1, 'params': {'model': config['image']['model'], 'resolution': config['image']['resolution'], 'aspect_ratio': '9:16', 'count': 1, 'prompt': shared + ' ' + prompt}} for i, prompt in enumerate(image_prompts)]
    videos = [{'index': i+1, 'params': {'model': config['video']['model'], 'resolution': config['video']['resolution'], 'duration': 10, 'aspect_ratio': '9:16', 'count': 1, 'prompt': shared + ' Motion begins in the first frame. ' + scene}, 'required_references': ['approved_environment_media_id', 'approved_mechanism_media_id'], 'submission_ready': False} for i, scene in enumerate(scenes)]
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'narration-script.txt').write_text(narration+'\n', encoding='utf-8')
    (output_dir / 'requests-draft.json').write_text(json.dumps({'not_for_direct_submission': True, 'images': images, 'videos': videos, 'note': 'Approve style, then generate matching assets using the actual approved style reference. Resolve all media IDs before any video submission. Re-time visuals from final Piljae speech.'}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    report = {'configuration_ready': True, 'generation_ready': False, 'paid_jobs_submitted': 0, 'voice': '필재', 'route': config['requested_route'], 'script_characters': len(narration), 'baseline_generation_credits': config['quote']['base_total'], 'typecast_process_key_present': bool(os.environ.get('TYPECAST_API_KEY', '').strip()), 'requires_live_checks': ['Higgsfield plan and usable credits', 'authenticated Piljae availability', 'measured Piljae audio', 'approved reference media'], 'output_directory': str(output_dir)}
    (output_dir / 'preparation-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / 'work/higgsfield-typecast')
    args = parser.parse_args()
    print(json.dumps(prepare(args.out), ensure_ascii=False, indent=2))
