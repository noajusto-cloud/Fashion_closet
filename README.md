# 👗 FASHION_CLOSET

## 📌 Overview

**FASHION_CLOSET** is a command-line wardrobe management system built in
Python.\
The system allows users to manage clothing items, create outfits, track
usage history, and integrate AI-based styling suggestions.

The project was designed following software engineering principles such
as **MVC architecture**, **Separation of Concerns (SoC)**, and
**Object-Oriented Programming (OOP)**.

------------------------------------------------------------------------

## 🏗 Architecture

The system is built using the **MVC (Model--View--Controller)** design
pattern:

-   **Models** -- Represent core entities such as `Garment` and
    `Outfit`.
-   **View (CLI)** -- Handles user interaction through a command-line
    interface.
-   **Controller** -- Manages business logic and coordinates between
    components.
-   **Database Layer** -- Encapsulates all data access logic using
    SQLite.
-   **AI Module** -- A separate module (`Ollama_Client`) for AI-based
    recommendations.

This structure ensures modularity, maintainability, and low coupling
between components.

------------------------------------------------------------------------

## ✨ Features

-   Add, update, and delete clothing items
-   Track last worn date
-   Detect unused garments
-   Create and manage outfits
-   Many-to-many relationship between outfits and garments
-   Mark outfits as worn (updates all included garments)
-   Clean CLI output using `tabulate`
-   AI integration for styling suggestions

------------------------------------------------------------------------

## 🧠 Design Principles

### 🔹 Object-Oriented Programming

The system is based on domain objects (`Garment`, `Outfit`) that
encapsulate both data and behavior.

### 🔹 Aggregation

An `Outfit` has-a collection of `Garment` objects.\
Garments exist independently even if an outfit is removed.

### 🔹 Low Coupling & Modularity

The AI service is separated into its own module, allowing future
replacement without affecting business logic.

### 🔹 Data Access Layer (DAO)

All database operations are centralized inside the `Database` class to
maintain separation between logic and persistence.

------------------------------------------------------------------------

## 🗄 Database Structure

The system uses SQLite with three tables:

-   `Garments`
-   `Outfits`
-   `Outfit_Items` (many-to-many relationship)

------------------------------------------------------------------------

## 🚀 Installation & Usage

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/yourusername/FASHION_CLOSET.git
cd FASHION_CLOSET
```

### 2️⃣ Install dependencies

``` bash
pip install tabulate
```

### 3️⃣ Run the application

``` bash
python main.py
```

------------------------------------------------------------------------

## 📚 Technologies Used

-   Python 3
-   SQLite
-   Tabulate
-   Ollama API (AI integration)

------------------------------------------------------------------------

## 🔮 Future Improvements

-   Web-based interface
-   User authentication system
-   Recommendation engine improvements
-   REST API layer
-   Dependency Injection implementation

------------------------------------------------------------------------

## 👩‍💻 Author

Developed as an academic software engineering project.
