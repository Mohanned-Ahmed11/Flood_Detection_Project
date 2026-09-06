import subprocess
import os
import matplotlib.pyplot as plt

def run_benchmark():
    exe_name = "flood_detection.exe"
    cpp_name = "flood_detection.cpp"

    print("Compiling C++ code...")
    compile_cmd = ["g++", "-O3", "-fopenmp", cpp_name, "-o", exe_name]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Compilation failed:", res.stderr)
        return

    print("Compilation successful. Starting benchmark suite...")

    threads_list = [1, 2, 4, 6, 8]
    grid_size = 3000 # 3000x3000 = 9 Megapixels

    results = []

    for t in threads_list:
        cmd = [f".\\{exe_name}", str(grid_size), str(grid_size), str(t)]
        res_run = subprocess.run(cmd, capture_output=True, text=True)
        out = res_run.stdout
        
        # Parse CSV_SUMMARY line
        for line in out.splitlines():
            if line.startswith("CSV_SUMMARY"):
                parts = line.split(",")
                size_str = parts[1]
                num_threads = int(parts[2])
                t_serial = float(parts[3])
                t_parallel = float(parts[4])
                speedup = float(parts[5])
                efficiency = float(parts[6])
                results.append({
                    "threads": num_threads,
                    "t_serial": t_serial,
                    "t_parallel": t_parallel,
                    "speedup": speedup,
                    "efficiency": efficiency
                })
                print(f"Threads: {num_threads:2d} | T_serial: {t_serial:7.2f} ms | T_parallel: {t_parallel:7.2f} ms | Speedup: {speedup:5.2f}x | Efficiency: {efficiency:5.1f}%")

    if not results:
        print("Error: No benchmark results collected.")
        return

    # Generate Plots
    threads = [r["threads"] for r in results]
    t_parallel = [r["t_parallel"] for r in results]
    speedups = [r["speedup"] for r in results]
    efficiencies = [r["efficiency"] for r in results]
    ideal_speedup = threads

    # Plot 1: Execution Time vs Threads
    plt.figure(figsize=(8, 5))
    plt.plot(threads, t_parallel, 'o-', color='#1f77b4', linewidth=2.5, markersize=8, label='Parallel Execution Time')
    plt.axhline(y=results[0]["t_serial"], color='#d62728', linestyle='--', label='Serial Baseline')
    plt.title(f'Execution Time vs Number of Threads ({grid_size}x{grid_size} Pixels)', fontsize=13, fontweight='bold')
    plt.xlabel('Number of Threads', fontsize=11)
    plt.ylabel('Execution Time (ms)', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig('flood_execution_time.png', dpi=300)
    plt.close()

    # Plot 2: Speedup vs Threads
    plt.figure(figsize=(8, 5))
    plt.plot(threads, speedups, 'o-', color='#2ca02c', linewidth=2.5, markersize=8, label='Measured Speedup (S)')
    plt.plot(threads, ideal_speedup, 'k--', linewidth=1.5, label='Ideal Linear Speedup')
    plt.title(f'Parallel Speedup vs Number of Threads ({grid_size}x{grid_size} Pixels)', fontsize=13, fontweight='bold')
    plt.xlabel('Number of Threads', fontsize=11)
    plt.ylabel('Speedup Factor (S)', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig('flood_speedup.png', dpi=300)
    plt.close()

    # Plot 3: Parallel Efficiency
    plt.figure(figsize=(8, 5))
    plt.plot(threads, efficiencies, 's-', color='#ff7f0e', linewidth=2.5, markersize=8, label='Parallel Efficiency (E)')
    plt.axhline(y=100, color='gray', linestyle=':')
    plt.title(f'Parallel Efficiency vs Number of Threads ({grid_size}x{grid_size} Pixels)', fontsize=13, fontweight='bold')
    plt.xlabel('Number of Threads', fontsize=11)
    plt.ylabel('Efficiency (%)', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig('flood_efficiency.png', dpi=300)
    plt.close()

    print("\nBenchmark completed! Generated plots:")
    print(" - flood_execution_time.png")
    print(" - flood_speedup.png")
    print(" - flood_efficiency.png")

if __name__ == "__main__":
    run_benchmark()
