This project is a Precision Agriculture platform designed to optimize crop yields by combining Machine Learning, Computer Vision, and Financial Analysis. It provides a comprehensive decision-making tool for modern farmers to manage irrigation, detect diseases, and forecast profitability.🌟 Key FeaturesPredictive AI Engine: Uses a Random Forest model to calculate precise irrigation needs based on soil temperature and humidity data.Drone Analysis (Computer Vision): Processes aerial imagery to detect plant vigor and vegetation stress using simulated NDVI (Normalized Difference Vegetation Index) analysis.Multi-Crop Management: Custom profiles for Tomatoes, Wheat, and Olives, including specific biological needs and market pricing.Automated Diagnostics: A digital "Prescription" system that identifies diseases (like Blight or Rust) and provides specific treatment dosages.Financial Dashboard: Real-time calculation of estimated yield (Tons/Hectare) and net profit projections after operational costs.🛠️ Technical StackComponentTechnologyUser InterfaceStreamlitAI FrameworkScikit-Learn (Random Forest Regressor)Image ProcessingOpenCV & Pillow (PIL)Data HandlingPandas & NumPyLanguagePython 3.x📋 Installation & SetupVirtual Environment:PowerShellpython -m venv venv
.\venv\Scripts\activate
Dependencies:PowerShell    pip install streamlit pandas numpy scikit-learn Pillow opencv-python
    ```

3.  **Generate Training Data**:
    Run the script to create the AI knowledge base:
    ```powershell
    python generer_data.py
    ```

4.  **Run the Application**:
    ```powershell
    streamlit run ia_agricole.py
    ```

---

## 📖 How it Works

### 1. Sensor Analysis
Users can toggle between **Live Weather** (simulated real-time data) or manual sliders to test various climatic scenarios. The AI then predicts the water requirement in L/m².

### 2. Drone Diagnostic
Upload an aerial field photo to trigger the computer vision module. The system converts images to RGB for universal compatibility and analyzes green-channel density to score plant health.

### 3. Financial Audit
The dashboard generates a financial summary, helping users understand the ROI (Return on Investment) based on current field conditions and crop types.

---

## 🎯 Project Objectives
*   **Yield Maximization**: Predicting the best harvest window and output.
*   **Resource Efficiency**: Reducing water waste and optimizing chemical treatments.
*   **Strategic Decision Making**: Providing clear, data-driven "Medical Prescriptions" for detected pathologies.

---

**Developed by:** Anas
**Academic Institution:** École Marocaine des Sciences de l'Ingénieur (EMSI)
**Specialization:** Computer Science & Networks
