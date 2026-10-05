from math import log2  # noqa: I001
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from microtonal_init_presets.lib import TEMPLATE_HELPERS
from config import Carlos, EDOs, EDTs, ED6s, ZPIs, FILTER_KEYTRK_OPTIONS

_ = (EDOs, EDTs, ED6s, Carlos, ZPIs)  # used in eval

loader = FileSystemLoader("templates")
env = Environment(loader = loader)
templates = list(map(
    env.get_template, env.list_templates()
))


def generate_tunings (
    tuning_group,  tuning_f,  harmonic = 2,
    get_x = lambda x: x,
    monopoly = lambda x: (8/x) - (1/6),
):
    log2h12 = log2(harmonic) * 12
    for x in eval(tuning_group):
        tuning = tuning_f(x)
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
    generate_tunings (
        "EDOs",
        lambda x: f"{x}-EDO"
    )
    generate_tunings (
        "EDTs",
        lambda x: f"{x}-EDT",
        harmonic = 3,
        monopoly = (lambda x: log2(3) * (8 / x) - (1/6)),
    )
    generate_tunings (
        "ED6s",
        lambda x: f"{x}-ED6",
        harmonic = 6,
        monopoly = (lambda x: log2(6) * (8 / x) - (1/6)),
    )
    generate_tunings (
        "ZPIs",
        lambda t: f"{t[0]}zpi",
        get_x = (lambda t: t[1]),
    )
    generate_tunings (
        "Carlos",
        lambda t: t[0],
        get_x = (lambda t: t[1]),
    )
