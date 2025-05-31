import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { Box } from "@chakra-ui/react";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import DashboardPage from "./pages/DashboardPage";
import BusinessSetupPage from "./pages/BusinessSetupPage";
import ContentGeneratorPage from "./pages/ContentGeneratorPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import SettingsPage from "./pages/SettingsPage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";

function App() {
  return (
    <Box minH="100vh">
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/app" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<Navigate to="/app" replace />} />
          <Route path="business/setup" element={<BusinessSetupPage />} />
          <Route path="content" element={<ContentGeneratorPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </Box>
  );
}

export default App;
