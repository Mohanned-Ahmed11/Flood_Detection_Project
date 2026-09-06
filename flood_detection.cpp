#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <iomanip>
#include <cstdlib>
#include <cstring>
#include <omp.h>

struct SpectralPixel {
    float green;
    float nir;
};

void generateSyntheticData(int width, int height, 
                           std::vector<SpectralPixel>& preFlood, 
                           std::vector<SpectralPixel>& postFlood) {
    size_t totalPixels = static_cast<size_t>(width) * height;
    preFlood.resize(totalPixels);
    postFlood.resize(totalPixels);

    #pragma omp parallel for schedule(static)
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            size_t idx = static_cast<size_t>(y) * width + x;

            float preG = 0.25f + 0.05f * std::sin(x * 0.01f);
            float preNIR = 0.65f + 0.05f * std::cos(y * 0.01f);

            bool isPermanentWater = (std::abs(y - (height / 2 + 50 * std::sin(x * 0.02f))) < 30);
            if (isPermanentWater) {
                preG = 0.55f;
                preNIR = 0.08f;
            }

            preFlood[idx] = {preG, preNIR};

            float postG = preG;
            float postNIR = preNIR;

            bool isFloodedZone = (x > width * 0.2 && x < width * 0.7 && 
                                 std::abs(y - height * 0.5) < height * 0.25);
            if (isFloodedZone && !isPermanentWater) {
                postG = 0.52f;
                postNIR = 0.09f;
            }

            postFlood[idx] = {postG, postNIR};
        }
    }
}

int processSerial(int width, int height, 
                  const std::vector<SpectralPixel>& preFlood, 
                  const std::vector<SpectralPixel>& postFlood, 
                  std::vector<uint8_t>& floodMask, 
                  float threshold = 0.0f) {
    size_t totalPixels = static_cast<size_t>(width) * height;
    int count = 0;

    for (size_t i = 0; i < totalPixels; ++i) {
        float preDenom = preFlood[i].green + preFlood[i].nir;
        float preNDWI = (preDenom > 1e-5f) ? (preFlood[i].green - preFlood[i].nir) / preDenom : -1.0f;
        bool preWater = (preNDWI > threshold);

        float postDenom = postFlood[i].green + postFlood[i].nir;
        float postNDWI = (postDenom > 1e-5f) ? (postFlood[i].green - postFlood[i].nir) / postDenom : -1.0f;
        bool postWater = (postNDWI > threshold);

        bool isFlooded = postWater && !preWater;
        floodMask[i] = isFlooded ? 255 : 0;

        if (isFlooded) {
            count++;
        }
    }
    return count;
}

int processParallel(int width, int height, 
                    const std::vector<SpectralPixel>& preFlood, 
                    const std::vector<SpectralPixel>& postFlood, 
                    std::vector<uint8_t>& floodMask, 
                    int numThreads, 
                    float threshold = 0.0f) {
    size_t totalPixels = static_cast<size_t>(width) * height;
    int count = 0;

    omp_set_num_threads(numThreads);

    #pragma omp parallel for schedule(dynamic, 4096) reduction(+:count)
    for (size_t i = 0; i < totalPixels; ++i) {
        float preDenom = preFlood[i].green + preFlood[i].nir;
        float preNDWI = (preDenom > 1e-5f) ? (preFlood[i].green - preFlood[i].nir) / preDenom : -1.0f;
        bool preWater = (preNDWI > threshold);

        float postDenom = postFlood[i].green + postFlood[i].nir;
        float postNDWI = (postDenom > 1e-5f) ? (postFlood[i].green - postFlood[i].nir) / postDenom : -1.0f;
        bool postWater = (postNDWI > threshold);

        bool isFlooded = postWater && !preWater;
        floodMask[i] = isFlooded ? 255 : 0;

        if (isFlooded) {
            count++;
        }
    }
    return count;
}

int main(int argc, char* argv[]) {
    int width = 3000;
    int height = 3000;
    int numThreads = 4;

    if (argc >= 3) {
        width = std::atoi(argv[1]);
        height = std::atoi(argv[2]);
    }
    if (argc >= 4) {
        numThreads = std::atoi(argv[3]);
    }

    size_t totalPixels = static_cast<size_t>(width) * height;

    std::vector<SpectralPixel> preFlood;
    std::vector<SpectralPixel> postFlood;
    generateSyntheticData(width, height, preFlood, postFlood);

    std::vector<uint8_t> maskSerial(totalPixels, 0);
    std::vector<uint8_t> maskParallel(totalPixels, 0);

    // Serial
    auto t1 = std::chrono::high_resolution_clock::now();
    int countSerial = processSerial(width, height, preFlood, postFlood, maskSerial);
    auto t2 = std::chrono::high_resolution_clock::now();
    double timeSerial = std::chrono::duration<double, std::milli>(t2 - t1).count();

    // Parallel
    auto t3 = std::chrono::high_resolution_clock::now();
    int countParallel = processParallel(width, height, preFlood, postFlood, maskParallel, numThreads);
    auto t4 = std::chrono::high_resolution_clock::now();
    double timeParallel = std::chrono::duration<double, std::milli>(t4 - t3).count();

    bool match = (countSerial == countParallel);
    double speedup = timeSerial / timeParallel;
    double efficiency = (speedup / numThreads) * 100.0;

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "CSV_SUMMARY," << width << "x" << height << "," << numThreads << "," 
              << timeSerial << "," << timeParallel << "," << speedup << "," << efficiency << "," << (match ? 1 : 0) << "\n";

    return 0;
}
