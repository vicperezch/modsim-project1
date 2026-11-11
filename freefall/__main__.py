import argparse

from . import plots, report, scenarios


def cmd_skydiver(args):
    runs = scenarios.run_skydiver(args.dt, args.metodo, args.altura or scenarios.SKYDIVER_HEIGHT)
    print(f"Paracaidista (método {args.metodo}, dt = {args.dt} s)\n")
    print(report.to_text(scenarios.skydiver_metrics(runs)))
    print(f"\nFigura: {plots.plot_skydiver(runs, args.salida)}")


def cmd_balls(args):
    runs, reference = scenarios.run_balls(args.dt, args.metodo, args.altura or scenarios.BALL_HEIGHT)
    print(f"Pelotas (método {args.metodo}, dt = {args.dt} s)\n")
    print(report.to_text(scenarios.ball_metrics(runs, reference)))
    print(f"\nFiguras: {plots.plot_ball_trajectories(runs, reference, args.salida)}")
    print(f"         {plots.plot_ball_summary(runs, reference, args.salida)}")


def build_parser():
    parser = argparse.ArgumentParser(prog="freefall", description="Simulación de caída libre con resistencia del aire")
    sub = parser.add_subparsers(dest="comando", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dt", type=float, default=0.01, help="paso de tiempo en segundos")
    common.add_argument("--metodo", choices=["rk4", "euler"], default="rk4", help="método de integración")
    common.add_argument("--altura", type=float, default=None, help="altura inicial en metros")
    common.add_argument("--salida", default="results", help="carpeta de salida")

    sub.add_parser("paracaidista", parents=[common], help="salto de paracaidista").set_defaults(func=cmd_skydiver)
    sub.add_parser("pelotas", parents=[common], help="comparación de pelotas").set_defaults(func=cmd_balls)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
