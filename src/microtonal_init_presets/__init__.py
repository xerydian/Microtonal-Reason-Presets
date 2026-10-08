from math import log2  # noqa: I001
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from microtonal_init_presets.lib import TEMPLATE_HELPERS
from config import Carlos, EDOs, EDFs, EDXs, ZPIs, FILTER_KEYTRK_OPTIONS

loader = FileSystemLoader("templates")
env = Environment(loader = loader)
templates = list(map(
    env.get_template, env.list_templates()
))


def generate_tunings (
    tuning_group, tuning_set, harmonic = 2,
    get_x = lambda x: x, tuning_f = None
):
    log2h = log2(harmonic)
    log2h12 = log2h * 12
    monopoly = lambda x: log2h * (8/x) - (1/6)
    for x in tuning_set:
        tuning = tuning_f(x) if tuning_f else f"{x}-{tuning_group[:3]}"
        tracking = log2h12 / get_x(x)
        inv_tracking = get_x(x) / (log2h12)
        x = get_x(x)
        for tmpl_name in env.list_templates():
            source, filename, _ = loader.get_source(env, tmpl_name)
            template = env.get_template(tmpl_name)

            filename = str(template.name).replace(".jinja", f" ({tuning}).repatch")
            has_filter = "filter_keytrk_factor" in source

            filepath = Path(tuning_group) / tuning / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)

            flt_kt_options = FILTER_KEYTRK_OPTIONS if has_filter else [FILTER_KEYTRK_OPTIONS[0]]

            for flt_kt_opt in flt_kt_options:
                filepath2 = filepath
                if has_filter:
                    filepath2 = filepath.with_stem(f"{filepath.stem} ({flt_kt_opt[1]})")

                with open(filepath2, "w") as f:
                    repatch = template.render( x = x,
                        tracking = tracking, inv_tracking = inv_tracking,  # avoid losing precision
                        monopoly = monopoly, filter_keytrk_factor = flt_kt_opt[0],
                        **TEMPLATE_HELPERS
                    )
                    f.write(repatch)


def main() -> None:
    generate_tunings ("EDFs", EDFs, harmonic = 3/2)
    generate_tunings ("EDOs", EDOs)
    for key, val in EDXs.items():
        generate_tunings (f"ED{key}s", val, harmonic=key)
    generate_tunings (
        "ZPIs", ZPIs,
        tuning_f = lambda t: f"{t[0]}zpi",
        get_x = (lambda t: t[1]),
    )
    generate_tunings (
        "Carlos", Carlos,
        tuning_f = lambda t: t[0],
        get_x = (lambda t: t[1]),
    )
