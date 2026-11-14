import argparse

from . import convergence, plots, report, scenarios


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


def cmd_convergence(args):
    print(f"Convergencia en [0, {args.t_final:g}] s contra la solución analítica\n")
    results = convergence.run_convergence(args.t_final)
    print(report.to_text(convergence.error_rows(results)))
    print()
    print(report.to_text(convergence.order_rows(results)))
    model, t, exact, runs = convergence.large_step_runs(args.dt_grande)
    print(f"\nFiguras: {plots.plot_convergence(results, args.salida)}")
    print(f"         {plots.plot_large_step(model, t, exact, runs, args.dt_grande, args.salida)}")


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
    conv = sub.add_parser("convergencia", help="análisis de convergencia de Euler y RK4")
    conv.add_argument("--t-final", type=float, default=20.0, help="intervalo de integración en segundos")
    conv.add_argument("--dt-grande", type=float, default=2.0, help="paso para la figura de comparación visual")
    conv.add_argument("--salida", default="results", help="carpeta de salida")
    conv.set_defaults(func=cmd_convergence)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
