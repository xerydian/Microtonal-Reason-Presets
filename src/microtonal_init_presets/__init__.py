from math import log2  # noqa: I001
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from microtonal_init_presets.lib import TEMPLATE_HELPERS
from config import Carlos, EDOs, EDTs, ED6s, ZPIs

_ = (EDOs, EDTs, ED6s, Carlos, ZPIs)  # used in eval

env = Environment(
    loader = FileSystemLoader("templates")
)
templates = list(map(
    env.get_template, env.list_templates()
))


def generate_tunings (
    tuning_group,  tuning_f,  harmonic = 2,
    get_x = lambda x: x,
    monopoly = lambda x: (8/x) - (1/6),
):
    for x in eval(tuning_group):
        tuning = tuning_f(x)
        for template in templates:
            filename = str(template.name).replace(".jinja", f" ({tuning}).repatch")
            filepath = Path(tuning_group) / tuning / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w") as f:
                repatch = template.render(
                    x = get_x(x),
                    tracking = (log2(harmonic) * 12 / get_x(x)),
                    inv_tracking = get_x(x) / (log2(harmonic) * 12),  # avoid losing precision
                    monopoly = monopoly, **TEMPLATE_HELPERS
                )
                f.write(repatch)


def main() -> None:
    generate_tunings (
        tuning_group = "EDOs",
        tuning_f = (lambda x: f"{x}-EDO"),
    )
    generate_tunings (
        tuning_group = "EDTs",
        tuning_f = (lambda x: f"{x}-EDT"),
        harmonic = 3,
        monopoly = (lambda x: log2(3) * (8 / x) - (1/6)),
    )
    generate_tunings (
        tuning_group = "ED6s",
        tuning_f = (lambda x: f"{x}-ED6"),
        harmonic = 6,
        monopoly = (lambda x: log2(6) * (8 / x) - (1/6)),
    )
    generate_tunings (
        tuning_group = "ZPIs",
        tuning_f = (lambda t: f"{t[0]}zpi"),
        get_x = (lambda t: t[1]),
    )
    generate_tunings (
        tuning_group = "Carlos",
        tuning_f = (lambda t: t[0]),
        get_x = (lambda t: t[1]),
    )
