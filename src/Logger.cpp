/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

#pragma once

class Logger {
private:
    std::ofstream logFile;
    std::stringstream logStream;

public:
    Logger() {
        logFile.open("C++_log.txt");
    }

    ~Logger() {
        logFile.close();
    }

    void log(const std::string& message) {
        logStream << message << "\n";
        logFile << message << std::endl;
        logFile.flush();  // Ensure the file is updated immediately
    }

    const std::string getLogs() const {
        return logStream.str();
    }
};
