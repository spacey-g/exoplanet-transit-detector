"""
bls_detector.py
---------------
Detect exoplanet transits from a CSV light curve using the 
Box Least Squares (BLS) algorithm.

Usage:
    python src/bls_detector.py sample-data/simulated_transit.csv
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.stats import BoxLeastSquares


# ---------------------------------------------------------
# Load CSV light curve
# ---------------------------------------------------------
def load_lightcurve(filepath):
    try:
        df = pd.read_csv(filepath)
    except:
        print(f"❌ Could not read file: {filepath}")
        sys.exit(1)

    if "time" not in df.columns or "flux" not in df.columns:
        print("❌ CSV must contain 'time' and 'flux' columns.")
        sys.exit(1)

    time = df["time"].values
    flux = df["flux"].values
    return time, flux


# ---------------------------------------------------------
# Run BLS
# ---------------------------------------------------------
def run_bls(time, flux):
    print("🔍 Running BLS...")

    periods = np.linspace(0.5, 10, 5000)  # Search range
    duration = 0.1                         # Transit duration (days)

    model = BoxLeastSquares(time, flux)
    results = model.power(periods, duration)

    best_period = results.period[np.argmax(results.power)]
    best_power = np.max(results.power)

    return results, best_period, best_power


# ---------------------------------------------------------
# Plot raw light curve
# ---------------------------------------------------------
def plot_raw(time, flux):
    plt.figure(figsize=(10, 4))
    plt.plot(time, flux, color="black", linewidth=0.7)
    plt.xlabel("Time (days)")
    plt.ylabel("Flux")
    plt.title("Raw Light Curve")
    plt.grid(True)
    plt.show()


# ---------------------------------------------------------
# Plot BLS periodogram
# ---------------------------------------------------------
def plot_bls(results, best_period):
    plt.figure(figsize=(10, 4))
    plt.plot(results.period, results.power, color="black")
    plt.axvline(best_period, color="red", linestyle="--", label=f"P = {best_period:.4f} d")
    plt.xlabel("Period (days)")
    plt.ylabel("BLS Power")
    plt.title("BLS Periodogram")
    plt.legend()
    plt.grid(True)
    plt.show()


# ---------------------------------------------------------
# Plot folded light curve
# ---------------------------------------------------------
def plot_folded(time, flux, best_period):
    phase = (time % best_period) / best_period

    plt.figure(figsize=(10, 4))
    plt.scatter(phase, flux, s=3, color="black")
    plt.xlabel("Phase")
    plt.ylabel("Flux")
    plt.title(f"Folded Light Curve (P = {best_period:.4f} d)")
    plt.grid(True)
    plt.show()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python src/bls_detector.py sample-data/simulated_transit.csv")
        sys.exit(1)

    filepath = sys.argv[1]

    time, flux = load_lightcurve(filepath)

    plot_raw(time, flux)

    results, best_period, best_power = run_bls(time, flux)

    print(f"✨ Best Period: {best_period:.6f} days")
    print(f"📊 BLS Power: {best_power:.3f}")

    plot_bls(results, best_period)
    plot_folded(time, flux, best_period)


if __name__ == "__main__":
    main()
