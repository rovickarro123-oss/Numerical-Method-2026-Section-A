import os
import sys
import webbrowser


def generate_interactive_ui(output_filename="app.html"):
    """Generates the single-page desktop application dashboard for Cube FEM Studio.

    Features:
      - Modern Pastel Pink Engineering Design Theme
      - Fully functional Ribbon Navigation (Home, File, Model, Loads, Analyze,
    Results, View, Export, Help)
      - Interactive 3D View and Load View Modes
      - Complete 3D Structural Frame / Space Truss FEM Solver Engine with dynamic
    matrix calculation
      - Real-time updates for Nodal Displacements, Support Reactions, Member
    Forces, and Audit Overlay
      - Clear, noticeable text sprites, force legends, and view cube triad
      - Overall label-size control with automatic SI/Imperial visual compensation
      - True elastic member deformation using 3D frame nodal translations and rotations
      - Undeformed/deformed overlay visualization with deformation scale
      - Re-expandable Left Properties Panel with visible toggle handle
      - Dynamic CSV/Excel report generation
    """
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cube FEM Studio - 3D Structural Frame Solver</title>
    <!-- Three.js & OrbitControls -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        :root {
            /* Pastel Pink Engineering Design System Palette */
            --pink-header-bg: #4A2231;
            --pink-ribbon-bg: #FCE4EC;
            --pink-ribbon-border: #F48FB1;
            --pink-accent: #D81B60;
            --pink-accent-hover: #C2185B;
            --pink-soft-bg: #FFF0F5;
            --pink-card-bg: #FFFFFF;
            --pink-border: #E6B8C8;
            --pink-active-tab: #F8BBD0;
            --pink-highlight: #FF4081;
            
            --text-main: #2D1F25;
            --text-muted: #7A5C68;
            --text-light: #FFFFFF;
            
            --panel-bg: #FAF3F6;
            --viewport-bg: #FFFFFF;
            --table-header-bg: #F8CCE0;
            --status-bar-bg: #381A25;
            
            --font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        }

        body.dark-theme {
            --pink-header-bg: #1A0C12;
            --pink-ribbon-bg: #2A1820;
            --pink-ribbon-border: #5C2C3E;
            --pink-accent: #FF4081;
            --pink-accent-hover: #F50057;
            --pink-soft-bg: #221219;
            --pink-card-bg: #2D1A23;
            --pink-border: #4A2837;
            --pink-active-tab: #3D2230;
            --text-main: #FCE4EC;
            --text-muted: #B3889B;
            --panel-bg: #201318;
            --viewport-bg: #150B0F;
            --table-header-bg: #3A1E2C;
            --status-bar-bg: #12070B;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body {
            font-family: var(--font-family);
            background-color: var(--panel-bg);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            font-size: 12px;
        }

        /* ---------------- A. TITLE BAR ---------------- */
        #title-bar {
            height: 34px;
            background-color: var(--pink-header-bg);
            color: var(--text-light);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 12px;
            font-size: 11px;
            border-bottom: 1px solid rgba(0,0,0,0.15);
        }

        #title-bar .app-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        #title-bar .app-logo {
            width: 18px;
            height: 18px;
            background: linear-gradient(135deg, var(--pink-highlight), var(--pink-accent));
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 10px;
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .save-status {
            font-size: 10px;
            background: rgba(255,255,255,0.18);
            padding: 2px 8px;
            border-radius: 10px;
            color: #F8BBD0;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .title-controls {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .theme-toggle-btn {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 3px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 10px;
            transition: all 0.2s;
        }
        .theme-toggle-btn:hover {
            background: rgba(255,255,255,0.2);
            border-color: #FFF;
        }

        /* ---------------- B. RIBBON NAVIGATION ---------------- */
        #ribbon-container {
            background-color: var(--pink-ribbon-bg);
            border-bottom: 2px solid var(--pink-ribbon-border);
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            z-index: 20;
        }

        #ribbon-tabs {
            display: flex;
            background-color: var(--pink-header-bg);
            padding-left: 8px;
        }

        .ribbon-tab {
            padding: 7px 16px;
            color: #E6B8C8;
            cursor: pointer;
            font-weight: 500;
            font-size: 11px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            transition: all 0.15s ease;
        }

        .ribbon-tab:hover {
            color: var(--text-light);
            background-color: rgba(255, 255, 255, 0.12);
        }

        .ribbon-tab.active {
            color: var(--pink-accent);
            background-color: var(--pink-ribbon-bg);
            font-weight: 700;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        }

        #ribbon-toolbar {
            height: 74px;
            padding: 6px 12px;
            display: flex;
            align-items: center;
            gap: 16px;
            overflow-x: auto;
        }

        .ribbon-panel {
            display: none;
            height: 100%;
            align-items: center;
            gap: 12px;
        }

        .ribbon-panel.active {
            display: flex;
        }

        .ribbon-group {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
            padding-right: 12px;
            border-right: 1px solid var(--pink-border);
        }

        .ribbon-group-title {
            font-size: 9px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            text-align: center;
            font-weight: 600;
        }

        .ribbon-buttons {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-grow: 1;
        }

        .ribbon-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: var(--pink-card-bg);
            border: 1px solid var(--pink-border);
            border-radius: 5px;
            padding: 4px 10px;
            min-width: 58px;
            height: 48px;
            cursor: pointer;
            color: var(--text-main);
            font-size: 10px;
            font-weight: 500;
            gap: 3px;
            transition: all 0.15s ease;
        }

        .ribbon-btn:hover {
            background-color: var(--pink-active-tab);
            border-color: var(--pink-accent);
            color: var(--pink-accent);
            transform: translateY(-1px);
        }

        .ribbon-btn.primary {
            background-color: var(--pink-accent);
            color: white;
            border-color: var(--pink-accent);
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(216, 27, 96, 0.25);
        }

        .ribbon-btn.primary:hover {
            background-color: var(--pink-accent-hover);
            box-shadow: 0 3px 6px rgba(216, 27, 96, 0.35);
        }

        .ribbon-btn svg {
            width: 16px;
            height: 16px;
            fill: currentColor;
        }

        .ribbon-input-container {
            display: flex;
            flex-direction: column;
            gap: 3px;
            font-size: 10px;
        }

        .ribbon-select, .ribbon-input {
            padding: 4px 8px;
            border: 1px solid var(--pink-border);
            border-radius: 4px;
            background: var(--pink-card-bg);
            color: var(--text-main);
            font-size: 11px;
            outline: none;
        }

        .ribbon-select:focus, .ribbon-input:focus {
            border-color: var(--pink-accent);
        }

        /* ---------------- C. MAIN WORKSPACE ---------------- */
        #workspace {
            display: flex;
            flex: 1 1 auto;
            min-height: 0;
            position: relative;
            overflow: hidden;
        }

        /* Re-expand button when left panel is collapsed */
        #left-panel-expand-btn {
            display: none;
            position: absolute;
            top: 10px;
            left: 0;
            z-index: 25;
            background: var(--pink-accent);
            color: white;
            border: none;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            padding: 8px 10px;
            cursor: pointer;
            font-weight: bold;
            font-size: 11px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
            transition: all 0.2s ease;
        }

        #left-panel-expand-btn:hover {
            background: var(--pink-accent-hover);
            padding-left: 14px;
        }

        /* LEFT PANEL: Properties & Explorer */
        #left-panel {
            width: 310px;
            min-height: 0;
            background-color: var(--panel-bg);
            border-right: 1px solid var(--pink-border);
            display: flex;
            flex-direction: column;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 10;
            position: relative;
        }

        #left-panel.collapsed {
            width: 0px;
            min-width: 0px;
            overflow: hidden;
            border-right: none;
            opacity: 0;
            pointer-events: none;
        }

        .panel-header {
            padding: 8px 12px;
            background-color: var(--pink-soft-bg);
            border-bottom: 1px solid var(--pink-border);
            font-weight: 700;
            color: var(--pink-accent);
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .panel-collapse-btn {
            background: rgba(216, 27, 96, 0.1);
            border: 1px solid var(--pink-border);
            border-radius: 4px;
            color: var(--pink-accent);
            padding: 2px 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 12px;
            transition: all 0.15s ease;
        }

        .panel-collapse-btn:hover {
            background: var(--pink-accent);
            color: white;
        }

        .panel-body {
            padding: 10px;
            overflow-y: auto;
            overflow-x: hidden;
            flex: 1 1 auto;
            min-height: 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .accordion-item {
            background: var(--pink-card-bg);
            border: 1px solid var(--pink-border);
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }

        .accordion-header {
            padding: 7px 10px;
            background: var(--pink-soft-bg);
            font-weight: 600;
            font-size: 11px;
            color: var(--text-main);
            border-bottom: 1px solid var(--pink-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .accordion-content {
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .form-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }

        .form-row label {
            font-size: 10px;
            color: var(--text-muted);
            flex-grow: 1;
            font-weight: 500;
        }

        .form-row input, .form-row select {
            width: 120px;
            padding: 4px 6px;
            border: 1px solid var(--pink-border);
            border-radius: 4px;
            font-size: 11px;
            background: var(--pink-card-bg);
            color: var(--text-main);
            outline: none;
        }

        .form-row input:focus, .form-row select:focus {
            border-color: var(--pink-accent);
        }

        /* CENTER PANEL: Interactive 3D Viewport & Views */
        #center-panel {
            flex: 1 1 auto;
            min-width: 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            position: relative;
            background-color: var(--viewport-bg);
        }

        /* Viewport Sub-header / Mode Tabs */
        #viewport-subbar {
            height: 38px;
            background: var(--pink-soft-bg);
            border-bottom: 1px solid var(--pink-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 12px;
            z-index: 5;
        }

        .view-mode-tabs {
            display: flex;
            gap: 4px;
            background: var(--pink-card-bg);
            padding: 3px;
            border-radius: 5px;
            border: 1px solid var(--pink-border);
        }

        .view-mode-tab {
            padding: 4px 16px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 11px;
            cursor: pointer;
            color: var(--text-muted);
            transition: all 0.15s ease;
        }

        .view-mode-tab:hover {
            color: var(--pink-accent);
        }

        .view-mode-tab.active {
            background-color: var(--pink-accent);
            color: white;
            box-shadow: 0 1px 4px rgba(216, 27, 96, 0.3);
        }

        .viewport-toolbar {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .v-btn {
            padding: 4px 10px;
            border: 1px solid var(--pink-border);
            border-radius: 4px;
            background: var(--pink-card-bg);
            color: var(--text-main);
            cursor: pointer;
            font-size: 10px;
            font-weight: 600;
            transition: all 0.15s ease;
        }
        .v-btn:hover {
            background: var(--pink-active-tab);
            border-color: var(--pink-accent);
            color: var(--pink-accent);
        }

        #viewport-canvas-container {
            flex: 1 1 auto;
            min-height: 0;
            position: relative;
            width: 100%;
            height: auto;
            overflow: hidden;
        }

        /* Floating Overlays on 3D Viewport */
        #plot-legend {
            position: absolute;
            top: 14px;
            left: 14px;
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid var(--pink-border);
            border-left: 4px solid var(--pink-accent);
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 10px;
            color: #2D1F25;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 5;
            pointer-events: none;
            min-width: 220px;
            backdrop-filter: blur(4px);
        }

        .legend-header {
            font-weight: bold;
            font-size: 11px;
            margin-bottom: 6px;
            color: var(--pink-accent);
            border-bottom: 1px solid var(--pink-border);
            padding-bottom: 4px;
        }

        .plot-legend-row {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
            font-weight: 500;
        }

        .plot-legend-line {
            width: 18px;
            height: 4px;
            border-radius: 2px;
            margin-right: 8px;
            display: inline-block;
        }

        #audit-overlay {
            position: absolute;
            top: 14px;
            right: 14px;
            width: 280px;
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid var(--pink-border);
            border-top: 4px solid var(--pink-accent);
            border-radius: 6px;
            padding: 10px 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            font-size: 10px;
            z-index: 5;
            backdrop-filter: blur(4px);
        }

        .audit-title {
            font-weight: 700;
            color: var(--pink-accent);
            margin-bottom: 6px;
            font-size: 11px;
            border-bottom: 1px solid var(--pink-border);
            padding-bottom: 4px;
            display: flex;
            justify-content: space-between;
        }

        /* BOTTOM PANEL: Results & Audit Tables */
        #bottom-panel {
            height: 200px;
            min-height: 28px;
            flex: 0 0 auto;
            background-color: var(--panel-bg);
            border-top: 2px solid var(--pink-border);
            display: flex;
            flex-direction: column;
            transition: height 0.25s ease;
            z-index: 10;
        }

        #bottom-panel.collapsed {
            height: 28px;
            overflow: hidden;
        }

        #bottom-tabs {
            display: flex;
            background: var(--pink-soft-bg);
            border-bottom: 1px solid var(--pink-border);
            padding-left: 8px;
        }

        .bottom-tab {
            padding: 6px 14px;
            font-size: 10px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-right: 1px solid var(--pink-border);
            transition: all 0.15s ease;
        }

        .bottom-tab:hover {
            color: var(--pink-accent);
        }

        .bottom-tab.active {
            background: var(--panel-bg);
            color: var(--pink-accent);
            border-top: 2px solid var(--pink-accent);
            font-weight: 700;
        }

        .bottom-tab-actions {
            margin-left: auto;
            display: flex;
            align-items: center;
            padding-right: 8px;
        }

        .toggle-bottom-btn {
            background: var(--pink-card-bg);
            border: 1px solid var(--pink-border);
            border-radius: 4px;
            padding: 2px 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 10px;
            color: var(--pink-accent);
            transition: all 0.15s ease;
        }

        .toggle-bottom-btn:hover {
            background: var(--pink-accent);
            color: white;
        }

        .bottom-content {
            flex-grow: 1;
            overflow: auto;
            padding: 6px;
        }

        /* Engineering Tables */
        table.eng-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            background: var(--pink-card-bg);
        }

        table.eng-table th {
            background-color: var(--table-header-bg);
            color: var(--text-main);
            font-weight: 700;
            padding: 6px 8px;
            border: 1px solid var(--pink-border);
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 2;
        }

        table.eng-table td {
            padding: 5px 8px;
            border: 1px solid var(--pink-border);
            text-align: center;
        }

        table.eng-table tr:nth-child(even) {
            background-color: var(--pink-soft-bg);
        }

        table.eng-table tr:hover {
            background-color: var(--pink-active-tab);
            cursor: pointer;
        }

        /* HOME DASHBOARD OVERLAY VIEW */
        #home-dashboard-view {
            display: none;
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: var(--panel-bg);
            z-index: 15;
            padding: 24px;
            overflow-y: auto;
        }

        #home-dashboard-view.active {
            display: block;
        }

        .dash-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .dash-card {
            background: var(--pink-card-bg);
            border: 1px solid var(--pink-border);
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            border-top: 4px solid var(--pink-accent);
            transition: transform 0.2s;
        }

        .dash-card:hover {
            transform: translateY(-2px);
        }

        .dash-card-title {
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .dash-card-value {
            font-size: 22px;
            font-weight: 700;
            color: var(--pink-accent);
            margin-top: 8px;
        }

        .dash-section {
            background: var(--pink-card-bg);
            border: 1px solid var(--pink-border);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }

        /* ---------------- D. STATUS BAR ---------------- */
        #status-bar {
            height: 26px;
            background-color: var(--status-bar-bg);
            color: #F8BBD0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 12px;
            font-size: 10px;
            border-top: 1px solid rgba(0,0,0,0.2);
            z-index: 30;
        }

        .status-segment {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .status-tag {
            background: rgba(255,255,255,0.15);
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 500;
        }

        /* ---------------- REV 5 VISUAL / UX OVERRIDES ---------------- */
        :root {
            --pink-accent: #d84f86;
            --pink-accent-hover: #bd3f72;
            --pink-highlight: #f59abb;
            --pink-soft-bg: #fff5f8;
            --pink-ribbon-bg: #fff8fb;
            --pink-ribbon-border: #efb5c9;
            --pink-border: #e7c4d0;
            --pink-active-tab: #fde0ea;
            --pink-card-bg: #ffffff;
            --viewport-bg: #fffdfd;
        }
        #ribbon-container { box-shadow: 0 3px 12px rgba(103,48,72,.08); }
        .ribbon-tab { padding: 8px 17px; letter-spacing:.15px; }
        .ribbon-btn { min-width: 66px; height: 50px; border-radius: 8px; box-shadow: 0 1px 2px rgba(60,20,40,.04); }
        .ribbon-btn.primary { box-shadow: 0 4px 10px rgba(216,79,134,.22); }
        .v-btn { border-radius: 7px; padding: 5px 11px; }
        #viewport-subbar { height: 44px; padding: 0 14px; background: linear-gradient(180deg,#fff8fb,#fff1f6); }
        .view-mode-tabs { border-radius: 8px; box-shadow: inset 0 0 0 1px rgba(231,196,208,.35); }
        .view-mode-tab { padding: 6px 18px; }
        .view-mode-tab.active { background: linear-gradient(180deg,#e05c91,#cf467d); }
        #plot-legend { min-width: 300px; max-width: 360px; padding: 13px 16px; border-radius: 10px; font-size: 12px; box-shadow: 0 8px 24px rgba(75,35,52,.15); }
        .legend-header { font-size: 13px; margin-bottom: 8px; }
        .plot-legend-row { margin-bottom: 7px; font-size: 12px; }
        .plot-legend-line { width: 25px; height: 5px; margin-right: 9px; }
        #audit-overlay { width: 310px; padding: 13px 16px; border-radius: 10px; font-size: 11px; box-shadow: 0 8px 24px rgba(75,35,52,.14); }
        .audit-title { font-size: 12px; }
        #left-panel-expand-btn { top: 14px; left: 6px; border-radius: 0 9px 9px 0; padding: 10px 13px; box-shadow: 0 5px 16px rgba(82,30,54,.2); }
        #left-panel-expand-btn:hover { padding-left: 17px; }
        #left-panel.collapsed { visibility: hidden; }
        #left-panel-expand-btn { pointer-events: auto; }
        .panel-header { padding: 10px 12px; }
        .accordion-item, .dash-card, .dash-section { border-radius: 9px; }
        #home-dashboard-view { padding: 26px; background: radial-gradient(circle at 80% 0%, #fff0f6 0%, var(--panel-bg) 42%); }
        .dash-card { box-shadow: 0 5px 18px rgba(91,44,63,.06); }
        .dash-card-value { font-size: 24px; }
        .load-summary-strip { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-top:8px; }
        .load-chip { display:inline-flex; align-items:center; gap:5px; padding:4px 8px; border-radius:999px; background:#fff4f8; border:1px solid #e7c4d0; font-size:10px; font-weight:700; color:#633244; }
        .load-chip b { color:#d84f86; }
        .view-control-card { position:absolute; left:14px; bottom:14px; z-index:6; background:rgba(255,255,255,.94); border:1px solid var(--pink-border); border-radius:10px; padding:9px 11px; box-shadow:0 6px 18px rgba(70,30,48,.10); font-size:10px; backdrop-filter:blur(5px); }
        .view-control-card label { display:flex; align-items:center; gap:7px; margin:4px 0; font-weight:600; color:#633244; }
        .view-control-card input[type=range] { width:105px; accent-color:var(--pink-accent); }
        .force-scale-value { min-width:35px; text-align:right; color:var(--pink-accent); }
        #status-bar { box-shadow: 0 -2px 8px rgba(50,20,35,.08); }
        @media (max-width: 1050px) { #audit-overlay { width:250px; } #plot-legend { min-width:240px; } .ribbon-btn { min-width:58px; } }

        /* REV 7 UI polish */
        #ribbon-tabs { gap: 2px; padding: 0 8px; }
        .ribbon-tab { position: relative; padding: 9px 17px 8px; border-bottom: 3px solid transparent; }
        .ribbon-tab.active { border-bottom-color: var(--pink-accent); background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(216,79,134,.10)); }
        .ribbon-tab.active::after { content:''; position:absolute; left:18%; right:18%; bottom:-3px; height:3px; background:var(--pink-accent); border-radius:3px 3px 0 0; }
        .ribbon-group { padding: 5px 14px 3px 2px; min-width: 0; }
        .ribbon-group-title { margin-top: 3px; }
        .ribbon-btn { transition: transform .16s ease, box-shadow .16s ease, background .16s ease, border-color .16s ease; }
        .ribbon-btn:hover { box-shadow: 0 5px 12px rgba(103,48,72,.10); }
        .ribbon-btn.primary { background: linear-gradient(180deg,#df5b90,#cf467d); }
        #left-panel { box-shadow: 4px 0 18px rgba(103,48,72,.05); }
        #bottom-panel { box-shadow: 0 -5px 18px rgba(103,48,72,.07); }
        .panel-body::-webkit-scrollbar, .bottom-content::-webkit-scrollbar { width: 8px; height: 8px; }
        .panel-body::-webkit-scrollbar-thumb, .bottom-content::-webkit-scrollbar-thumb { background:#e6b8c8; border-radius:999px; }
        .panel-body::-webkit-scrollbar-track, .bottom-content::-webkit-scrollbar-track { background:#fff5f8; }
        .accordion-item { flex: 0 0 auto; }
        .accordion-content { overflow: visible; }
        .view-control-card { min-width: 260px; }
        .force-scale-help { font-size:9px; color:#8a6877; margin-top:2px; line-height:1.35; }

        /* REV 7 PHASE 2 */
        .result-mode-select { min-width:145px; height:30px; border:1px solid var(--pink-border); border-radius:7px; background:#fff; color:var(--text-main); padding:0 8px; font-size:10px; font-weight:600; }
        .diagram-scale-help { font-size:9px; color:#8a6877; margin-top:2px; line-height:1.3; }
        .reference-plane-badge { position:absolute; right:14px; bottom:14px; z-index:6; padding:7px 9px; border:1px solid var(--pink-border); border-radius:8px; background:rgba(255,255,255,.92); color:#633244; font-size:9px; box-shadow:0 5px 16px rgba(70,30,48,.08); pointer-events:none; }
        .phase2-chip { display:inline-flex; align-items:center; gap:5px; padding:3px 7px; border-radius:999px; background:#fff4f8; border:1px solid #e7c4d0; color:#633244; font-size:9px; font-weight:700; }
        .phase2-chip b { color:var(--pink-accent); }
        #left-panel .panel-body { min-height:0; flex:1 1 auto; overflow-y:auto; overflow-x:hidden; overscroll-behavior:contain; padding-bottom:18px; }
        #workspace,#center-panel,#left-panel { min-height:0; }
        #bottom-panel { min-width:0; }
    </style>
</head>
<body>
    <input type="file" id="project-file-input" accept=".json,application/json" style="display:none" onchange="loadProjectFile(event)">

    <!-- A. TITLE BAR -->
    <div id="title-bar">
        <div class="app-title">
            <span class="app-logo">3D</span>
            <span>Cube FEM Studio</span>
            <span style="opacity:0.5;">|</span>
            <span id="project-title-text">Cube Frame Structural Solver Model.fem</span>
            <span class="save-status" id="save-indicator">Saved</span>
        </div>
        <div class="title-controls">
            <button class="theme-toggle-btn" onclick="toggleTheme()">Toggle Theme</button>
            <span style="opacity:0.85; font-size:10px;">Unit System: <strong id="title-unit-display" style="color:#FF80AB;">SI (kN, m, mm, MPa)</strong></span>
        </div>
    </div>

    <!-- B. RIBBON NAVIGATION -->
    <div id="ribbon-container">
        <div id="ribbon-tabs">
            <div class="ribbon-tab active" onclick="switchRibbonTab('home')">Home</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('file')">File</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('model')">Model</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('loads')">Loads</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('analyze')">Analyze</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('results')">Results</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('view')">View</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('export')">Export</div>
            <div class="ribbon-tab" onclick="switchRibbonTab('help')">Help</div>
        </div>

        <div id="ribbon-toolbar">
            <!-- HOME TAB -->
            <div class="ribbon-panel active" id="panel-home">
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn primary" onclick="runRev3Solver()">
                            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                            Run Solver
                        </button>
                        <button class="ribbon-btn" onclick="switchRibbonTab('results'); switchBottomTab('displacements');">
                            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/></svg>
                            Results
                        </button>
                        <button class="ribbon-btn" onclick="exportToExcelCSV()">
                            <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                            Export Excel
                        </button>
                    </div>
                    <div class="ribbon-group-title">Quick Actions</div>
                </div>

                <div class="ribbon-group">
                    <div class="ribbon-input-container">
                        <label>Active Unit System:</label>
                        <select class="ribbon-select" id="unit-system-select" onchange="toggleUnits()">
                            <option value="SI">SI System (kN, m, mm, MPa)</option>
                            <option value="IMP">Imperial System (kip, ft, in, ksi)</option>
                        </select>
                    </div>
                    <div class="ribbon-group-title">Unit System</div>
                </div>

                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="toggleDashboardOverlay()">Dashboard View</button>
                        <button class="ribbon-btn" onclick="resetCameraView()">Reset View</button>
                    </div>
                    <div class="ribbon-group-title">Workspace</div>
                </div>
            </div>

            <!-- FILE TAB -->
            <div class="ribbon-panel" id="panel-file">
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="newProject()">New Project</button>
                        <button class="ribbon-btn" onclick="openProjectPicker()">Open Project</button>
                        <button class="ribbon-btn" onclick="saveProject()">Save Project</button>
                        <button class="ribbon-btn" onclick="saveProject()">Save As</button>
                    </div>
                    <div class="ribbon-group-title">Project Management</div>
                </div>
            </div>

            <!-- MODEL TAB -->
            <div class="ribbon-panel" id="panel-model">
                <div class="ribbon-group">
                    <div class="ribbon-input-container">
                        <label>Cube Dimension (L):</label>
                        <input type="number" class="ribbon-input" id="cube-dim-input" value="6.0" step="0.5" onchange="updateCubeDimensions()">
                    </div>
                    <div class="ribbon-group-title">Geometry</div>
                </div>
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="switchBottomTab('nodes')">Nodes Table</button>
                        <button class="ribbon-btn" onclick="switchBottomTab('members')">Members Table</button>
                    </div>
                    <div class="ribbon-group-title">Elements</div>
                </div>
            </div>

            <!-- LOADS TAB -->
            <div class="ribbon-panel" id="panel-loads">
                <div class="ribbon-group">
                    <div class="ribbon-input-container">
                        <label>Active Load Case / Combination:</label>
                        <select class="ribbon-select" id="active-loadcase" onchange="updateLoadCaseView()">
                            <option value="COMB1">COMB1: 1.4D (LRFD Combination 1 - 1.4D)</option>
                            <option value="LC1">LC1: DEAD / SELF WEIGHT (Self-Weight Y: -1)</option>
                            <option value="LC2">LC2: ROOF DEAD (5 kN/m Uniform Y)</option>
                            <option value="LC3">LC3: ROOF LIVE (3 kN/m Uniform Y)</option>
                            <option value="LC4">LC4: ROOF CENTER POINT LOAD (5 kN Y)</option>
                            <option value="LC5">LC5: WIND X (10 kN Total / Roof Nodes)</option>
                            <option value="LC6">LC6: WIND Z (10 kN Total / Roof Nodes)</option>
                            <option value="LC7">LC7: SEISMIC X (15 kN Total / Roof Nodes)</option>
                            <option value="LC8">LC8: SEISMIC Z (15 kN Total / Roof Nodes)</option>
                            <option value="COMB2">COMB2: 1.2D + 1.6L (LRFD Combo 2)</option>
                            <option value="COMB_ASD1">COMB_ASD1: D + L (ASD Combo 1)</option>
                        </select>
                    </div>
                    <div class="ribbon-group-title">Load Cases</div>
                </div>
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="applyDiaphragmConstraint()">Apply Diaphragm</button>
                    </div>
                    <div class="ribbon-group-title">Constraints</div>
                </div>
            </div>

            <!-- ANALYZE TAB -->
            <div class="ribbon-panel" id="panel-analyze">
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn primary" onclick="runRev3Solver()">Run Matrix Analysis</button>
                        <button class="ribbon-btn" onclick="validateModel()">Validate Model</button>
                    </div>
                    <div class="ribbon-group-title">Matrix Engine</div>
                </div>
            </div>

            <!-- RESULTS TAB -->
            <div class="ribbon-panel" id="panel-results">
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="switchBottomTab('displacements')">Displacements</button>
                        <button class="ribbon-btn" onclick="switchBottomTab('reactions')">Reactions</button>
                        <button class="ribbon-btn" onclick="switchBottomTab('member_forces')">Member Forces</button>
                    </div>
                    <div class="ribbon-group-title">Output Tables</div>
                </div>
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <select class="result-mode-select" id="result-diagram-select" onchange="setResultDiagram(this.value)">
                            <option value="none">No Diagram</option><option value="axial">Axial Force N</option><option value="shearY">Shear Vy</option><option value="shearZ">Shear Vz</option><option value="momentY">Moment My</option><option value="momentZ">Moment Mz</option><option value="torsion">Torsion T</option>
                        </select>
                        <button class="ribbon-btn" onclick="setResultDiagram('none')">Clear Diagram</button>
                    </div>
                    <div class="ribbon-group-title">Internal Force Diagrams</div>
                </div>
            </div>

            <!-- VIEW TAB -->
            <div class="ribbon-panel" id="panel-view">
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="setCameraPreset('iso')">Isometric</button>
                        <button class="ribbon-btn" onclick="setCameraPreset('top')">Top</button>
                        <button class="ribbon-btn" onclick="setCameraPreset('front')">Front</button>
                        <button class="ribbon-btn" onclick="setCameraPreset('right')">Right</button>
                    </div>
                    <div class="ribbon-group-title">Camera Views</div>
                </div>
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="toggleVisibility('nodes')">Nodes</button>
                        <button class="ribbon-btn" onclick="toggleVisibility('members')">Members</button>
                        <button class="ribbon-btn" onclick="toggleVisibility('loads')">Loads</button>
                        <button class="ribbon-btn" onclick="toggleVisibility('legend')">Legend</button>
                        <button class="ribbon-btn" onclick="toggleReferencePlanes()">Reference Planes</button>
                    </div>
                    <div class="ribbon-group-title">Visibility</div>
                </div>
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="toggleDisplayOption('forceLabels')">Force Labels</button>
                        <button class="ribbon-btn" onclick="toggleDisplayOption('deformed')">Deformed</button>
                        <button class="ribbon-btn" onclick="toggleDisplayOption('reactions')">Reactions</button>
                    </div>
                    <div class="ribbon-group-title">Analysis Graphics</div>
                </div>
            </div>

            <!-- EXPORT TAB -->
            <div class="ribbon-panel" id="panel-export">
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn primary" onclick="exportToExcelCSV()">Export Excel / CSV</button>
                    </div>
                    <div class="ribbon-group-title">Reports</div>
                </div>
            </div>

            <!-- HELP TAB -->
            <div class="ribbon-panel" id="panel-help">
                <div class="ribbon-group">
                    <div class="ribbon-buttons">
                        <button class="ribbon-btn" onclick="showAbout()">About Solver</button>
                    </div>
                    <div class="ribbon-group-title">Documentation</div>
                </div>
            </div>
        </div>
    </div>

    <!-- C. MAIN WORKSPACE -->
    <div id="workspace">
        <!-- Re-expand Button when Left Panel is Collapsed -->
        <button id="left-panel-expand-btn" onclick="toggleLeftPanel()">▶ Properties & Inputs</button>

        <!-- HOME DASHBOARD OVERLAY VIEW -->
        <div id="home-dashboard-view">
            <h2 style="color: var(--pink-accent); margin-bottom: 14px; font-size: 16px; font-weight: 700;">Cube Structural Solver Executive Dashboard</h2>
            <div class="dash-cards-grid">
                <div class="dash-card">
                    <div class="dash-card-title">Number of Nodes</div>
                    <div class="dash-card-value" id="dash-node-count">8</div>
                </div>
                <div class="dash-card">
                    <div class="dash-card-title">Number of Members</div>
                    <div class="dash-card-value" id="dash-member-count">12</div>
                </div>
                <div class="dash-card">
                    <div class="dash-card-title">Number of Supports</div>
                    <div class="dash-card-value">4 (Fixed Base)</div>
                </div>
                <div class="dash-card">
                    <div class="dash-card-title">Active Load Case</div>
                    <div class="dash-card-value" id="dash-active-lc" style="font-size:15px; margin-top:8px;">COMB1 (1.4D)</div>
                </div>
                <div class="dash-card">
                    <div class="dash-card-title">Max Displacement</div>
                    <div class="dash-card-value" id="dash-max-disp">0.576 mm</div>
                </div>
                <div class="dash-card">
                    <div class="dash-card-title">Max Member Force</div>
                    <div class="dash-card-value" id="dash-max-force">0.00 kN</div>
                </div>
                <div class="dash-card">
                    <div class="dash-card-title">Load Components</div>
                    <div class="dash-card-value" id="dash-load-components" style="font-size:11px;line-height:1.5;">ΣFx 0 · ΣFy 0 · ΣFz 0 kN</div>
                </div>
                <div class="dash-card">
                    <div class="dash-card-title">Analysis Status</div>
                    <div class="dash-card-value" id="dash-solver-status" style="color:#2E7D32; font-size:15px; margin-top:8px;">Converged</div>
                </div>
            </div>

            <div class="dash-section">
                <h3 style="margin-bottom: 10px; color: var(--pink-accent); font-size: 14px;">Quick Analysis Actions</h3>
                <p style="margin-bottom: 14px; color: var(--text-muted); font-size: 11px;">Configure parameters, select load cases, or run full matrix stiffness analysis on the 3D frame model.</p>
                <div style="display:flex; gap:12px;">
                    <button class="ribbon-btn primary" onclick="toggleDashboardOverlay(); runRev3Solver();" style="height:38px; padding:0 24px; font-size:11px;">Run 3D Frame Solver</button>
                    <button class="ribbon-btn" onclick="toggleDashboardOverlay(); switchRibbonTab('loads');" style="height:38px; padding:0 24px; font-size:11px;">Configure Load Cases</button>
                    <button class="ribbon-btn" onclick="toggleDashboardOverlay(); exportToExcelCSV();" style="height:38px; padding:0 24px; font-size:11px;">Export Calculation CSV</button>
                </div>
            </div>
        </div>

        <!-- LEFT PANEL: Context Properties & Settings -->
        <div id="left-panel">
            <div class="panel-header">
                <span>Properties & Inputs</span>
                <button class="panel-collapse-btn" onclick="toggleLeftPanel()">◀</button>
            </div>
            <div class="panel-body">

                <!-- Project Info -->
                <div class="accordion-item">
                    <div class="accordion-header">Project Information</div>
                    <div class="accordion-content">
                        <div class="form-row"><label>Model Name:</label><input type="text" id="proj-name" value="Cube 6 m Model"></div>
                        <div class="form-row"><label>Engineer:</label><input type="text" value="Structural Engineer"></div>
                    </div>
                </div>

                <!-- Section & Material Properties -->
                <div class="accordion-item">
                    <div class="accordion-header">Material & Section</div>
                    <div class="accordion-content">
                        <div class="form-row"><label id="lbl-mat-e">E [MPa]:</label><input type="number" id="mat-e" value="200000" onchange="runRev3Solver()"></div>
                        <div class="form-row"><label id="lbl-mat-dens">Density [kN/m³]:</label><input type="number" id="mat-dens" value="24.0" onchange="runRev3Solver()"></div>
                        <div class="form-row"><label id="lbl-sec-b">Width b [mm]:</label><input type="number" id="sec-b" value="300" onchange="runRev3Solver()"></div>
                        <div class="form-row"><label id="lbl-sec-h">Depth h [mm]:</label><input type="number" id="sec-h" value="450" onchange="runRev3Solver()"></div>
                    </div>
                </div>

                <!-- Diaphragm Constraint -->
                <div class="accordion-item">
                    <div class="accordion-header">Rigid Diaphragm</div>
                    <div class="accordion-content">
                        <div class="form-row"><label id="lbl-diaphragm-elevation">Elevation (Y):</label><input type="number" id="diaphragm-elevation" value="6.0" step="0.5"></div>
                        <div class="form-row"><label>Master Node:</label><input type="number" id="diaphragm-master" value="5"></div>
                        <button class="ribbon-btn" style="width:100%; height:30px; margin-top:4px;" onclick="applyDiaphragmConstraint()">Apply Diaphragm Coupling</button>
                    </div>
                </div>

                <!-- Selected Object Inspector -->
                <div class="accordion-item">
                    <div class="accordion-header">Selection Inspector</div>
                    <div class="accordion-content" id="selection-inspector-body">
                        <span style="color: var(--text-muted); font-size:10px;">Click any node or member in the 3D viewport to view properties.</span>
                    </div>
                </div>

            </div>
        </div>

        <!-- CENTER PANEL: Viewport & View Mode Tabs -->
        <div id="center-panel">
            <div id="viewport-subbar">
                <!-- REQUIRED: 3D View and Load View Tabs -->
                <div class="view-mode-tabs">
                    <div class="view-mode-tab active" id="tab-mode-3d" onclick="switchViewMode('3D')">3D View</div>
                    <div class="view-mode-tab" id="tab-mode-load" onclick="switchViewMode('LOAD')">Load View</div>
                </div>

                <div class="viewport-toolbar">
                    <button class="v-btn" onclick="setCameraPreset('iso')">Isometric</button>
                    <button class="v-btn" onclick="setCameraPreset('top')">Top View</button>
                    <button class="v-btn" onclick="setCameraPreset('front')">Front View</button>
                    <button class="v-btn" onclick="resetCameraView()">Fit Model</button>
                </div>
            </div>

            <div id="viewport-canvas-container">
                <!-- Matplotlib / Engineering Style Plot Legend Overlay -->
                <div id="plot-legend">
                    <div class="legend-header" id="plot-title">Load Analysis: COMB1</div>
                    <div id="plot-legend-content"></div>
                </div>

                <div class="view-control-card">
                    <strong style="color:var(--pink-accent);">Graphics Controls</strong>
                    <label><input type="checkbox" id="chk-force-labels" checked onchange="setDisplayOption('forceLabels', this.checked)"> Member force magnitudes</label>
                    <label><input type="checkbox" id="chk-load-labels" checked onchange="setDisplayOption('loadLabels', this.checked)"> Load magnitudes</label>
                    <label><input type="checkbox" id="chk-deformed-overlay" onchange="setDisplayOption('deformedOverlay', this.checked)"> Deformed overlay</label>
                    <label><span>Force glyph scale</span><input id="force-scale" type="range" min="0.5" max="2.5" step="0.1" value="1" oninput="setForceScale(this.value)"><span class="force-scale-value" id="force-scale-value">1.0×</span></label>
                    <div class="force-scale-help">Changes the visual length/size of load and reaction arrows only; numerical forces stay unchanged.</div>
                    <label><span>Deformation scale</span><input id="deform-scale" type="range" min="1" max="100" step="1" value="20" oninput="setDeformScale(this.value)"><span class="force-scale-value" id="deform-scale-value">20×</span></label>
                    <label><span>Label size</span><input id="label-scale" type="range" min="0.50" max="3.00" step="0.05" value="1.00" oninput="setLabelScale(this.value)"><span class="force-scale-value" id="label-scale-value">1.00×</span></label>
                    <label><span>Result diagram</span><select class="result-mode-select" style="width:150px;" id="result-diagram-inline" onchange="setResultDiagram(this.value)"><option value="none">None</option><option value="axial">Axial N</option><option value="shearY">Shear Vy</option><option value="shearZ">Shear Vz</option><option value="momentY">Moment My</option><option value="momentZ">Moment Mz</option><option value="torsion">Torsion T</option></select></label>
                    <label><span>Diagram scale</span><input id="diagram-scale" type="range" min="0.15" max="1.00" step="0.05" value="0.35" oninput="setDiagramScale(this.value)"><span class="force-scale-value" id="diagram-scale-value">0.35×</span></label>
                    <div class="diagram-scale-help">Phase 2 diagrams are normalized for readable 3D presentation; numerical results remain unchanged.</div>
                </div>
                <div class="reference-plane-badge" id="reference-plane-badge">Reference planes: XZ · YZ · XY</div>

                <!-- Audit Overlay Box -->
                <div id="audit-overlay">
                    <div class="audit-title">
                        <span>REV 3 VERIFICATION & AUDIT</span>
                        <span style="color:#2E7D32; font-weight:bold;">[PASS]</span>
                    </div>
                    <div style="line-height:1.6;">
                        <strong>Active Load Case:</strong> <span id="audit-lc-name" style="color:var(--pink-accent); font-weight:700;">COMB1 (1.4D)</span><br>
                        <strong>Total Applied Force:</strong> <span id="audit-total-load" style="color:#2E7D32; font-weight:700;">0.000 kN</span><br>
                        <strong>Equilibrium Error:</strong> <span id="audit-eq-error" style="color:#2E7D32; font-weight:700;">0.000 kN (Pass)</span><br>
                        <strong>Max Frame Deflection:</strong> <span id="max-def" style="color:#2E7D32; font-weight:700;">0.576 mm</span><br>
                        <strong>Solver Status:</strong> <span id="solver-status" style="color:#2E7D32; font-weight:700;">Converged</span>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- BOTTOM PANEL: Engineering Results Tables -->
    <div id="bottom-panel">
        <div id="bottom-tabs">
            <div class="bottom-tab active" id="btab-displacements" onclick="switchBottomTab('displacements')">Nodal Displacements</div>
            <div class="bottom-tab" id="btab-reactions" onclick="switchBottomTab('reactions')">Support Reactions</div>
            <div class="bottom-tab" id="btab-member_forces" onclick="switchBottomTab('member_forces')">Member Forces</div>
            <div class="bottom-tab" id="btab-nodes" onclick="switchBottomTab('nodes')">Node Coordinates</div>
            <div class="bottom-tab" id="btab-members" onclick="switchBottomTab('members')">Member Connectivity</div>
            <div class="bottom-tab" id="btab-audit" onclick="switchBottomTab('audit')">Analysis Log</div>
            <div class="bottom-tab-actions">
                <button class="toggle-bottom-btn" onclick="toggleBottomPanel()">▲ / ▼ Panel</button>
            </div>
        </div>

        <div class="bottom-content" id="bottom-table-container">
            <!-- Dynamic table content generated by solver -->
        </div>
    </div>

    <!-- D. STATUS BAR -->
    <div id="status-bar">
        <div class="status-segment">
            <span class="status-tag" id="sb-unit">Unit: SI</span>
            <span id="sb-project">Project: Cube Frame Structural Solver Model.fem</span>
            <span id="sb-selection">Selected: None</span>
        </div>
        <div class="status-segment">
            <span id="sb-status" style="color:#81C784; font-weight:600;">Solver Status: Ready</span>
            <span class="status-tag">3D Engine: Three.js WebGL</span>
        </div>
    </div>

<script>
    // System State Variables
    let isImperial = false;
    let currentViewMode = '3D'; // '3D' or 'LOAD'
    let selectedEntity = null;
    let visibility = { nodes: true, members: true, loads: true, legend: true };
    let displayOptions = { forceLabels: true, loadLabels: true, deformed: false, reactions: false };
    let forceScale = 1.0;
    let deformScale = 20.0;
    let labelScale = 1.0; // overall 3D label size multiplier
    let resultDiagramMode = 'none';
    let diagramScale = 0.35;
    let referencePlanesVisible = true
    let diaphragmEnabled = false;
    let lastSolveError = '';

    // Structure Geometry Data
    let cubeDim = 6.0; // default 6 meters
    let nodes = {
        1: [0, 0, 0], 2: [6, 0, 0], 3: [6, 0, 6], 4: [0, 0, 6],
        5: [0, 6, 0], 6: [6, 6, 0], 7: [6, 6, 6], 8: [0, 6, 6]
    };

    let elements = [
        { id: 'M1', nodes: [1, 2], type: 'Base Beam' },
        { id: 'M2', nodes: [2, 3], type: 'Base Beam' },
        { id: 'M3', nodes: [3, 4], type: 'Base Beam' },
        { id: 'M4', nodes: [4, 1], type: 'Base Beam' },
        { id: 'M5', nodes: [5, 6], type: 'Roof Beam' },
        { id: 'M6', nodes: [6, 7], type: 'Roof Beam' },
        { id: 'M7', nodes: [7, 8], type: 'Roof Beam' },
        { id: 'M8', nodes: [8, 5], type: 'Roof Beam' },
        { id: 'M9', nodes: [1, 5], type: 'Column' },
        { id: 'M10', nodes: [2, 6], type: 'Column' },
        { id: 'M11', nodes: [3, 7], type: 'Column' },
        { id: 'M12', nodes: [4, 8], type: 'Column' }
    ];

    // Current Computed Analysis Results
    let computedResults = {
        displacements: {},
        displacementModel: {},
        reactions: {},
        memberForces: {},
        totalAppliedForce: 0.0,
        maxDeflection: 0.0,
        equilibriumError: 0.0,
        loadComponents: {Fx:0,Fy:0,Fz:0,magnitude:0},
        memberEndForces: {},
        memberEndDisplacements: {}
    };

    // Three.js Scene Setup
    const container = document.getElementById('viewport-canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xFFFFFF);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(15, 12, 16);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.target.set(3, 3, 3);
    controls.update();

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.4);
    dirLight.position.set(12, 24, 18);
    scene.add(dirLight);

    const modelGroup = new THREE.Group();
    scene.add(modelGroup);

    const loadGraphicsGroup = new THREE.Group();
    scene.add(loadGraphicsGroup);

    // Raycaster for object selection
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    renderer.domElement.addEventListener('click', onViewportClick, false);

    function onViewportClick(event) {
        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(modelGroup.children, true);

        if (intersects.length > 0) {
            let hit = intersects[0].object;
            while (hit && !hit.userData.type && hit.parent) {
                hit = hit.parent;
            }
            if (hit && hit.userData && hit.userData.type) {
                selectedEntity = hit.userData;
                updateSelectionInspector();
            }
        }
    }

    function updateSelectionInspector() {
        const inspector = document.getElementById('selection-inspector-body');
        const sbSel = document.getElementById('sb-selection');

        if (!selectedEntity) {
            inspector.innerHTML = `<span style="color: var(--text-muted); font-size:10px;">Click any node or member in 3D to inspect properties.</span>`;
            sbSel.innerText = 'Selected: None';
            return;
        }

        if (selectedEntity.type === 'node') {
            const id = selectedEntity.id;
            const [x, y, z] = nodes[id];
            const disp = computedResults.displacements[id] || [0, 0, 0];
            sbSel.innerText = `Selected: Node N${id}`;
            inspector.innerHTML = `
                <div class="form-row"><strong>Type:</strong> <span>Structural Node</span></div>
                <div class="form-row"><strong>Node ID:</strong> <span>N${id}</span></div>
                <div class="form-row"><strong>X Coord:</strong> <span>${x.toFixed(2)} ${isImperial?'ft':'m'}</span></div>
                <div class="form-row"><strong>Y Coord:</strong> <span>${y.toFixed(2)} ${isImperial?'ft':'m'}</span></div>
                <div class="form-row"><strong>Z Coord:</strong> <span>${z.toFixed(2)} ${isImperial?'ft':'m'}</span></div>
                <div class="form-row"><strong>Condition:</strong> <span>${y === 0 ? 'Fixed Base' : 'Free / Diaphragm'}</span></div>
                <div class="form-row"><strong>Disp Y:</strong> <span>${disp[1].toFixed(3)} ${isImperial?'in':'mm'}</span></div>
            `;
        } else if (selectedEntity.type === 'member') {
            const id = selectedEntity.id;
            const elem = elements.find(e => e.id === id);
            const force = computedResults.memberForces[id] || 0;
            const endForce = computedResults.memberEndForces[id] || {i:[0,0,0,0,0,0],j:[0,0,0,0,0,0]};
            const b = document.getElementById('sec-b').value;
            const h = document.getElementById('sec-h').value;
            sbSel.innerText = `Selected: Member ${id}`;
            inspector.innerHTML = `
                <div class="form-row"><strong>Type:</strong> <span>${elem.type}</span></div>
                <div class="form-row"><strong>Member ID:</strong> <span>${id}</span></div>
                <div class="form-row"><strong>Start Node:</strong> <span>N${elem.nodes[0]}</span></div>
                <div class="form-row"><strong>End Node:</strong> <span>N${elem.nodes[1]}</span></div>
                <div class="form-row"><strong>Section:</strong> <span>${b}x${h} ${isImperial?'in':'mm'}</span></div>
                <div class="form-row"><strong>Axial Force:</strong> <span>${force.toFixed(3)} ${isImperial?'kip':'kN'}</span></div>
                <div class="form-row"><strong>Start Shear Vy/Vz:</strong> <span>${endForce.i[1].toFixed(3)} / ${endForce.i[2].toFixed(3)} ${isImperial?'kip':'kN'}</span></div>
                <div class="form-row"><strong>Start Moment My/Mz:</strong> <span>${endForce.i[4].toFixed(3)} / ${endForce.i[5].toFixed(3)} ${isImperial?'kip-ft':'kN·m'}</span></div>
                <div class="form-row"><strong>Status:</strong> <span>${force < -0.01 ? 'Compression' : force > 0.01 ? 'Tension' : 'Near Zero'}</span></div>
            `;
        }
    }

    // High-contrast, zoom-friendly engineering label sprite.
    function createTextSprite(text, colorHex, position, scale = 1.0, bgBox = true) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = 420 * dpr;
        canvas.height = 120 * dpr;
        context.scale(dpr, dpr);
        if (bgBox) {
            context.fillStyle = 'rgba(255,255,255,0.96)';
            context.strokeStyle = colorHex;
            context.lineWidth = 3;
            context.beginPath();
            if (context.roundRect) context.roundRect(8, 10, 404, 100, 12);
            else context.rect(8, 10, 404, 100);
            context.fill(); context.stroke();
        }
        context.font = '700 34px "Segoe UI", Arial, sans-serif';
        context.fillStyle = colorHex;
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(String(text), 210, 60);
        const texture = new THREE.CanvasTexture(canvas);
        texture.minFilter = THREE.LinearFilter;
        texture.magFilter = THREE.LinearFilter;
        texture.needsUpdate = true;
        const material = new THREE.SpriteMaterial({ map: texture, depthTest: false, depthWrite: false, transparent: true });
        const sprite = new THREE.Sprite(material);
        sprite.position.copy(position);
        // Keep labels visually consistent when the model changes from metres to feet.
        // The slider is the user's overall label-size control.
        const unitComp = Math.max(1, cubeDim / 6.0);
        const finalScale = scale * labelScale * unitComp;
        sprite.scale.set(1.72 * finalScale, 0.49 * finalScale, 1);
        sprite.userData = { type: 'label' };
        return sprite;
    }

    // Grid & Coordinate Triad Axis    // Grid & Coordinate Triad Axis
    let referenceGridGroup = null;
    function create3DGridPlanes() {
        if(referenceGridGroup) scene.remove(referenceGridGroup);
        const gridGroup = new THREE.Group(); referenceGridGroup=gridGroup;
        if(!referencePlanesVisible){ scene.add(gridGroup); return; }
        const L=cubeDim, divisions=Math.max(4,Math.round(L));
        const xz=new THREE.GridHelper(L*1.18,divisions,0xD84F86,0xE8CBD6); xz.position.set(L/2,-0.025,L/2); gridGroup.add(xz);
        const yz=new THREE.GridHelper(L*1.18,divisions,0x6A4C93,0xE5D9E9); yz.rotation.z=Math.PI/2; yz.position.set(-0.025,L/2,L/2); gridGroup.add(yz);
        const xy=new THREE.GridHelper(L*1.18,divisions,0x4C78A8,0xD9E4EE); xy.rotation.x=Math.PI/2; xy.position.set(L/2,L/2,-0.025); gridGroup.add(xy);
        const pm=(c)=>new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:.035,side:THREE.DoubleSide,depthWrite:false});
        const p0=new THREE.Mesh(new THREE.PlaneGeometry(L*1.18,L*1.18),pm(0xD84F86)); p0.rotation.x=-Math.PI/2; p0.position.set(L/2,-0.035,L/2); gridGroup.add(p0);
        const p1=new THREE.Mesh(new THREE.PlaneGeometry(L*1.18,L*1.18),pm(0x6A4C93)); p1.rotation.y=Math.PI/2; p1.position.set(-0.035,L/2,L/2); gridGroup.add(p1);
        const p2=new THREE.Mesh(new THREE.PlaneGeometry(L*1.18,L*1.18),pm(0x4C78A8)); p2.position.set(L/2,L/2,-0.035); gridGroup.add(p2);
        const o=new THREE.Vector3(-1.15,-0.15,-1.15);
        gridGroup.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),o,1.5,0xD84F86,.3,.15));
        gridGroup.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),o,1.5,0x4C78A8,.3,.15));
        gridGroup.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1),o,1.5,0x6A4C93,.3,.15));
        gridGroup.add(createTextSprite('X','#D84F86',o.clone().add(new THREE.Vector3(1.7,0,0)),.4,false));
        gridGroup.add(createTextSprite('Y','#4C78A8',o.clone().add(new THREE.Vector3(0,1.7,0)),.4,false));
        gridGroup.add(createTextSprite('Z','#6A4C93',o.clone().add(new THREE.Vector3(0,0,1.7)),.4,false));
        gridGroup.add(createTextSprite('X-Z PLANE','#D84F86',new THREE.Vector3(L*.82,-.12,L*.72),.27,false));
        gridGroup.add(createTextSprite('Y-Z PLANE','#6A4C93',new THREE.Vector3(-.15,L*.72,L*.72),.27,false));
        gridGroup.add(createTextSprite('X-Y PLANE','#4C78A8',new THREE.Vector3(L*.72,L*.72,-.15),.27,false));
        scene.add(gridGroup);
    }
    create3DGridPlanes();

    // RENDER 3D MODEL
    function forceColor(force) {
        if (force < -0.001) return 0xd64545; // compression
        if (force > 0.001) return 0x3478c9; // tension
        return 0x68717c;
    }

    function formatForce(v) {
        const unit = isImperial ? 'kip' : 'kN';
        return `${Math.abs(v).toFixed(2)} ${unit}`;
    }

    function localToGlobalPoint(p1, R, localOffset){
        // R rows are the member local x/y/z unit axes expressed in global coordinates.
        // Convert a local displacement/offset back to global coordinates with R^T.
        return new THREE.Vector3(
            p1[0] + R[0][0]*localOffset[0] + R[1][0]*localOffset[1] + R[2][0]*localOffset[2],
            p1[1] + R[0][1]*localOffset[0] + R[1][1]*localOffset[1] + R[2][1]*localOffset[2],
            p1[2] + R[0][2]*localOffset[0] + R[1][2]*localOffset[1] + R[2][2]*localOffset[2]
        );
    }

    function elasticMemberLocalPoint(elem,t){
        const p1=nodes[elem.nodes[0]], m=memberCacheForVisualization(elem), L=m.L, ed=computedResults.memberEndDisplacements?.[elem.id];
        if(!ed) return new THREE.Vector3(...p1);
        const visualScale=(displayOptions.deformed||displayOptions.deformedOverlay)?deformScale:0;
        t=Math.max(0,Math.min(1,t)); const x=t*L, x2=t*t, x3=x2*t, ui=ed.i, uj=ed.j;
        const u=(1-t)*ui[0]+t*uj[0];
        const Nv1=1-3*x2+2*x3, Nv2=L*(t-2*x2+x3), Nv3=3*x2-2*x3, Nv4=L*(-x2+x3);
        const v=Nv1*ui[1]+Nv2*ui[5]+Nv3*uj[1]+Nv4*uj[5];
        const w=Nv1*ui[2]-Nv2*ui[4]+Nv3*uj[2]-Nv4*uj[4];
        return localToGlobalPoint(p1,m.R,[x+visualScale*u,visualScale*v,visualScale*w]);
    }
    function hermiteElasticMemberPoints(elem,segments=48){ const pts=[]; for(let k=0;k<=segments;k++) pts.push(elasticMemberLocalPoint(elem,k/segments)); return pts; }
    function createElasticMemberCurve(elem){ const curve=new THREE.Curve(); curve.getPoint=function(t){return elasticMemberLocalPoint(elem,t);}; return curve; }
    function memberCacheForVisualization(elem){ const p1=nodes[elem.nodes[0]],p2=nodes[elem.nodes[1]],tr=frameTransformation(p1,p2); return {L:norm3([p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]),R:tr.R}; }
    function addMemberTube(pointsOrCurve,color,radius=.075,userData=null,transparent=false){ const curve=(pointsOrCurve&&typeof pointsOrCurve.getPoint==='function')?pointsOrCurve:new THREE.CatmullRomCurve3(pointsOrCurve); const geom=new THREE.TubeGeometry(curve,48,radius,10,false); const mat=new THREE.MeshStandardMaterial({color,roughness:.34,metalness:.12,transparent,opacity:transparent?.30:1}); const mesh=new THREE.Mesh(geom,mat); if(userData)mesh.userData=userData; modelGroup.add(mesh); return mesh; }

    function renderModel() {
        while(modelGroup.children.length > 0) modelGroup.remove(modelGroup.children[0]);
        while(loadGraphicsGroup.children.length > 0) loadGraphicsGroup.remove(loadGraphicsGroup.children[0]);

        const showDeformed = displayOptions.deformed || displayOptions.deformedOverlay;
        const getPos = (id, deformed=false) => {
            const base = new THREE.Vector3(...nodes[id]);
            if (!deformed) return base;
            const d = computedResults.displacementModel?.[id] || [0,0,0];
            return base.add(new THREE.Vector3(d[0], d[1], d[2]).multiplyScalar(deformScale));
        };

        // When deformation is enabled, retain the original frame as a light reference overlay.
        if (showDeformed && visibility.members) {
            elements.forEach(elem=>{
                const p1=new THREE.Vector3(...nodes[elem.nodes[0]]), p2=new THREE.Vector3(...nodes[elem.nodes[1]]);
                const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints([p1,p2]),new THREE.LineBasicMaterial({color:0x9e9e9e,transparent:true,opacity:.32}));
                line.userData={type:'undeformed-reference',id:elem.id};
                modelGroup.add(line);
            });
        }

        if (visibility.members) {
            elements.forEach(elem => {
                const force = computedResults.memberForces[elem.id] || 0;
                const memberColor = forceColor(force);
                const userData={type:'member',id:elem.id};
                if(showDeformed){
                    addMemberTube(createElasticMemberCurve(elem),memberColor,.095,userData,false);
                    modelGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(hermiteElasticMemberPoints(elem,48)),new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.42,depthTest:false})));
                }else{
                    const p1 = getPos(elem.nodes[0], false), p2 = getPos(elem.nodes[1], false);
                    const dir = new THREE.Vector3().subVectors(p2,p1);
                    const len = dir.length();
                    const geom = new THREE.CylinderGeometry(0.075,0.075,len,12);
                    const mat = new THREE.MeshStandardMaterial({ color: memberColor, roughness:0.34, metalness:0.12 });
                    const cyl = new THREE.Mesh(geom,mat);
                    cyl.position.copy(p1).add(dir.clone().multiplyScalar(0.5));
                    cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.clone().normalize());
                    cyl.userData=userData;
                    modelGroup.add(cyl);
                }

                const mid = showDeformed ? hermiteElasticMemberPoints(elem,48)[24] || hermiteElasticMemberPoints(elem,48)[0] : getPos(elem.nodes[0],false).add(getPos(elem.nodes[1],false)).multiplyScalar(.5);
                if (displayOptions.forceLabels && Math.abs(force) > 0.001) {
                    const offset = new THREE.Vector3(0,0.24,0);
                    modelGroup.add(createTextSprite(`${elem.id}  ${force >= 0 ? 'T' : 'C'} ${formatForce(force)}`, force >= 0 ? '#3478C9' : '#D64545', mid.clone().add(offset), 0.52));
                } else {
                    modelGroup.add(createTextSprite(elem.id, '#6B3A4E', mid.clone().add(new THREE.Vector3(0,0.22,0)), 0.40));
                }
            });
        }

        if (visibility.nodes) {
            Object.keys(nodes).forEach(id => {
                const pos = getPos(parseInt(id), showDeformed);
                const y = nodes[id][1];
                const geom = new THREE.SphereGeometry(0.24,18,18);
                const mat = new THREE.MeshStandardMaterial({color:y===0?0x7c4d9e:0xd84f86,roughness:0.28,metalness:0.18});
                const sphere = new THREE.Mesh(geom,mat);
                sphere.position.copy(pos);
                sphere.userData={type:'node',id:parseInt(id)};
                modelGroup.add(sphere);
                if (y===0) {
                    const box = new THREE.Mesh(new THREE.BoxGeometry(0.54,0.16,0.54),new THREE.MeshStandardMaterial({color:0x55306e,roughness:.4}));
                    box.position.copy(pos).add(new THREE.Vector3(0,-0.10,0));
                    modelGroup.add(box);
                }
                modelGroup.add(createTextSprite(`N${id}`, '#2c2227', pos.clone().add(new THREE.Vector3(.38,.28,.35)), .46));
            });
        }

        const roofNodeIds=[5,6,7,8];
        const roofPts=roofNodeIds.map(id=>getPos(id,showDeformed)); roofPts.push(roofPts[0]);
        modelGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(roofPts),new THREE.LineBasicMaterial({color:0xd84f86,transparent:true,opacity:.7})));

        if (displayOptions.reactions) renderReactionGraphics();
        if (visibility.loads) renderLoadVisuals(document.getElementById('active-loadcase').value);
        if (resultDiagramMode !== 'none') renderResultDiagrams();
        updateForceLegend();
    }

    function diagramValueForMember(elem,mode,t){ const ef=computedResults.memberEndForces?.[elem.id]||{i:[0,0,0,0,0,0],j:[0,0,0,0,0,0]}; const i=ef.i,j=ef.j; if(mode==='axial')return(1-t)*i[0]+t*(-j[0]); if(mode==='shearY')return(1-t)*i[1]+t*(-j[1]); if(mode==='shearZ')return(1-t)*i[2]+t*(-j[2]); if(mode==='torsion')return(1-t)*i[3]+t*(-j[3]); if(mode==='momentY')return(1-t)*i[4]+t*(-j[4]); if(mode==='momentZ')return(1-t)*i[5]+t*(-j[5]); return 0; }
    function diagramMeta(mode){ const m={axial:['N','kN',0x3478c9],shearY:['Vy','kN',0x43a047],shearZ:['Vz','kN',0x43a047],momentY:['My','kN·m',0xd84f86],momentZ:['Mz','kN·m',0xd84f86],torsion:['T','kN·m',0x7b4fa3]}; const a=m[mode]||m.axial; return {name:a[0],unit:isImperial?(a[1]==='kN'?'kip':'kip-ft'):a[1],color:a[2]}; }
    function renderResultDiagrams(){ const vals=[]; elements.forEach(e=>{for(let k=0;k<=24;k++)vals.push(Math.abs(diagramValueForMember(e,resultDiagramMode,k/24)));}); const maxAbs=Math.max(...vals,1e-9), meta=diagramMeta(resultDiagramMode), diagramLength=cubeDim*.55*diagramScale; elements.forEach(elem=>{ const basePts=[],diagPts=[],m=memberCacheForVisualization(elem); for(let k=0;k<=24;k++){ const t=k/24,base=elasticMemberLocalPoint(elem,t),val=diagramValueForMember(elem,resultDiagramMode,t),amp=val/maxAbs*diagramLength; let off=[0,amp,0]; if(resultDiagramMode==='shearZ'||resultDiagramMode==='momentY')off=[0,0,amp]; const gp=localToGlobalPoint([base.x,base.y,base.z],m.R,off); basePts.push(base);diagPts.push(gp); } modelGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(diagPts),new THREE.LineBasicMaterial({color:meta.color,transparent:true,opacity:.95}))); const verts=[]; for(let k=0;k<24;k++){const a=basePts[k],b=basePts[k+1],c=diagPts[k+1],d=diagPts[k]; verts.push(a.x,a.y,a.z,b.x,b.y,b.z,c.x,c.y,c.z,a.x,a.y,a.z,c.x,c.y,c.z,d.x,d.y,d.z);} const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(new Float32Array(verts),3));modelGroup.add(new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:meta.color,transparent:true,opacity:.10,side:THREE.DoubleSide,depthWrite:false}))); }); document.getElementById('plot-title').innerText=`${meta.name} DIAGRAM • ${document.getElementById('active-loadcase').value}`; document.getElementById('plot-legend-content').innerHTML=`<div class="phase2-chip">RESULT <b>${meta.name}</b></div><div style="margin-top:7px;line-height:1.5">Scale: <b>${diagramScale.toFixed(2)}×</b><br>Governing magnitude: <b>${maxAbs.toFixed(2)} ${meta.unit}</b><br><span style="color:#8a6877">Diagram scale is visual only; numerical results remain unchanged.</span></div>`; }

    function renderReactionGraphics() {
        const scale = forceScale;
        Object.keys(computedResults.reactions || {}).forEach(id=>{
            const r=computedResults.reactions[id];
            const p=new THREE.Vector3(...nodes[id]);
            const mag=Math.sqrt(r[0]*r[0]+r[1]*r[1]+r[2]*r[2]);
            if(mag<1e-7) return;
            const dir=new THREE.Vector3(r[0],r[1],r[2]).normalize();
            const len=Math.min(cubeDim*0.42,(0.55+Math.log10(1+mag))*scale);
            loadGraphicsGroup.add(new THREE.ArrowHelper(dir,p,len,0x7b4fa3,0.18*Math.sqrt(scale),0.10*Math.sqrt(scale)));
            if(displayOptions.forceLabels) loadGraphicsGroup.add(createTextSprite(`R${id} ${mag.toFixed(2)} ${isImperial?'kip':'kN'}`,'#7b4fa3',p.clone().add(dir.clone().multiplyScalar(len+.25)),.42));
        });
    }

    function addDistributedLoadCurtain(p1,p2,height,labelText,colorHex,magnitude=0) {
        const dir=new THREE.Vector3(0,1,0);
        const glyphHeight=Math.max(0.08,Math.min(cubeDim*0.32,height*forceScale));
        const p1t=p1.clone().addScaledVector(dir,glyphHeight), p2t=p2.clone().addScaledVector(dir,glyphHeight);
        const vertices=new Float32Array([p1.x,p1.y,p1.z,p2.x,p2.y,p2.z,p2t.x,p2t.y,p2t.z,p1.x,p1.y,p1.z,p2t.x,p2t.y,p2t.z,p1t.x,p1t.y,p1t.z]);
        const geom=new THREE.BufferGeometry(); geom.setAttribute('position',new THREE.BufferAttribute(vertices,3));
        loadGraphicsGroup.add(new THREE.Mesh(geom,new THREE.MeshBasicMaterial({color:colorHex,transparent:true,opacity:.30,side:THREE.DoubleSide})));
        for(let t=.08;t<=.92;t+=.17){
            const pt=p1t.clone().lerp(p2t,t);
            loadGraphicsGroup.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),pt,glyphHeight,colorHex,.18*Math.sqrt(forceScale),.11*Math.sqrt(forceScale)));
        }
        if(labelText && displayOptions.loadLabels){
            const mid=p1t.clone().add(p2t).multiplyScalar(.5).add(new THREE.Vector3(0,.12,0));
            loadGraphicsGroup.add(createTextSprite(labelText,colorHex,mid,.47));
        }
    }

    function addPointLoadVector(pos,dir,colorHex,labelText,magnitude=0) {
        const arrowLen=Math.min(cubeDim*.50,(.85+Math.log10(1+Math.abs(magnitude))*.7)*forceScale);
        const unit=dir.clone().normalize();
        const start=pos.clone().sub(unit.clone().multiplyScalar(arrowLen));
        loadGraphicsGroup.add(new THREE.ArrowHelper(unit,start,arrowLen,colorHex,.26*Math.sqrt(forceScale),.15*Math.sqrt(forceScale)));
        if(labelText && displayOptions.loadLabels) loadGraphicsGroup.add(createTextSprite(labelText,colorHex,start.clone().sub(unit.clone().multiplyScalar(.28)),.48));
    }

    function getLoadDefinition(lc) {
        const density=parseFloat(document.getElementById('mat-dens').value)||24;
        const b=parseFloat(document.getElementById('sec-b').value)||300;
        const h=parseFloat(document.getElementById('sec-h').value)||450;
        const A=isImperial?(b*h)/144:(b*h)/1e6;
        const selfWPerM=isImperial ? density*A : density*A; // kip/ft or kN/m
        const D={selfWeight:true,roofDead:true,roofDeadW:5};
        const L={roofLiveW:3,centerPoint:5};
        const def={Fx:0,Fy:0,Fz:0,desc:'',factorD:0,factorL:0,source:lc};
        if(lc==='LC1'){def.factorD=1;def.desc='Dead / self weight';}
        else if(lc==='LC2'){def.factorD=1;def.roofDeadOnly=true;def.desc='Roof dead load';}
        else if(lc==='LC3'){def.factorL=1;def.liveOnly=true;def.desc='Roof live load';}
        else if(lc==='LC4'){def.factorL=1;def.pointOnly=true;def.desc='Roof center point load';}
        else if(lc==='LC5'){def.Fx=10;def.lateralOnly='X';def.desc='Wind +X';}
        else if(lc==='LC6'){def.Fz=10;def.lateralOnly='Z';def.desc='Wind +Z';}
        else if(lc==='LC7'){def.Fx=15;def.lateralOnly='X';def.desc='Seismic +X';}
        else if(lc==='LC8'){def.Fz=15;def.lateralOnly='Z';def.desc='Seismic +Z';}
        else if(lc==='COMB1'){def.factorD=1.4;def.desc='1.4D';}
        else if(lc==='COMB2'){def.factorD=1.2;def.factorL=1.6;def.desc='1.2D + 1.6L';}
        else if(lc==='COMB_ASD1'){def.factorD=1;def.factorL=1;def.desc='D + L';}
        def.selfWPerM=selfWPerM; return def;
    }

    function renderLoadVisuals(lc) {
        const legendContent=document.getElementById('plot-legend-content');
        const def=getLoadDefinition(lc);
        const fUnit=isImperial?'kip':'kN', wUnit=isImperial?'kip/ft':'kN/m';
        document.getElementById('plot-title').innerText=`Load View • ${lc}`;
        const comps=computedResults.loadComponents || {Fx:0,Fy:0,Fz:0,magnitude:0};
        legendContent.innerHTML=`
          <div class="plot-legend-row"><span class="plot-legend-line" style="background:#d84f86"></span>Vertical distributed / point loads</div>
          <div class="plot-legend-row"><span class="plot-legend-line" style="background:#3478c9"></span>+X lateral loads</div>
          <div class="plot-legend-row"><span class="plot-legend-line" style="background:#43a047"></span>+Z lateral loads</div>
          <div style="margin-top:7px;padding-top:7px;border-top:1px solid #e7c4d0;line-height:1.65">
            <b>${lc}</b> — ${def.desc}<br>
            ΣFx: <b>${comps.Fx.toFixed(2)} ${fUnit}</b> &nbsp; ΣFy: <b>${comps.Fy.toFixed(2)} ${fUnit}</b><br>
            ΣFz: <b>${comps.Fz.toFixed(2)} ${fUnit}</b> &nbsp; |F|: <b>${comps.magnitude.toFixed(2)} ${fUnit}</b>
          </div>`;

        const roofBeams=[[5,6],[6,7],[7,8],[8,5]];
        const addRoofW=(w,color,name)=>roofBeams.forEach(e=>{
            const p1=new THREE.Vector3(...nodes[e[0]]),p2=new THREE.Vector3(...nodes[e[1]]);
            addDistributedLoadCurtain(p1,p2,Math.max(.55,cubeDim*.10),`${name} ${w.toFixed(2)} ${wUnit}`,color,w);
        });
        const addSelfWeight=()=>elements.forEach(e=>{
            const p1=new THREE.Vector3(...nodes[e.nodes[0]]),p2=new THREE.Vector3(...nodes[e.nodes[1]]);
            const L=p1.distanceTo(p2); const w=def.selfWPerM;
            if(w>0) addDistributedLoadCurtain(p1,p2,Math.max(.30,cubeDim*.055),`SW ${w.toFixed(2)} ${wUnit}`,'#c85b88',w);
        });
        if(def.factorD>0){
            if(lc==='LC1' || lc==='COMB1' || lc==='COMB2' || lc==='COMB_ASD1') addSelfWeight();
            if(!def.liveOnly) addRoofW(5*def.factorD,'#d84f86','D');
        }
        if(def.factorL>0){
            if(lc==='LC4'){
                const q=5*def.factorL; const center=new THREE.Vector3(cubeDim/2,cubeDim,cubeDim/2);
                addPointLoadVector(center,new THREE.Vector3(0,-1,0),'#d84f86',`P ${q.toFixed(2)} ${fUnit}`,q);
            } else addRoofW(3*def.factorL,'#e46c9b','L');
        }
        if(def.lateralOnly==='X') [5,6,7,8].forEach(id=>addPointLoadVector(new THREE.Vector3(...nodes[id]),new THREE.Vector3(1,0,0),'#3478c9',`${def.Fx.toFixed(2)} ${fUnit}`,def.Fx));
        if(def.lateralOnly==='Z') [5,6,7,8].forEach(id=>addPointLoadVector(new THREE.Vector3(...nodes[id]),new THREE.Vector3(0,0,1),'#43a047',`${def.Fz.toFixed(2)} ${fUnit}`,def.Fz));
    }

    function updateForceLegend(){
        if(!visibility.legend) return;
        const fUnit=isImperial?'kip':'kN';
        let vals=Object.values(computedResults.memberForces||{});
        let maxT=vals.length?Math.max(0,...vals):0, maxC=vals.length?Math.max(0,...vals.map(v=>-v)):0;
        const lc=document.getElementById('active-loadcase').value;
        document.getElementById('plot-legend').style.display='block';
        const el=document.getElementById('plot-legend-content');
        if(currentViewMode==='3D'){
            el.innerHTML=`<div class="plot-legend-row"><span class="plot-legend-line" style="background:#3478c9"></span> Tension — <b>${maxT.toFixed(2)} ${fUnit}</b> max</div>
            <div class="plot-legend-row"><span class="plot-legend-line" style="background:#d64545"></span> Compression — <b>${maxC.toFixed(2)} ${fUnit}</b> max</div>
            <div class="plot-legend-row"><span class="plot-legend-line" style="background:#68717c"></span> Near-zero axial force</div>
            <div style="margin-top:7px;color:#765064">Active: <b>${lc}</b> · Labels ${displayOptions.forceLabels?'ON':'OFF'}</div>`;
        }
    }

    // ---------------- REV 5 TRUE 3D FRAME MATRIX ENGINE ----------------
    // 6 DOF per node: UX, UY, UZ, RX, RY, RZ. Euler-Bernoulli frame stiffness.
    function zeros(n,m){ return Array.from({length:n},()=>Array(m).fill(0)); }
    function dot3(a,b){ return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]; }
    function norm3(a){ return Math.sqrt(dot3(a,a)); }
    function normalize3(a){ const n=norm3(a)||1; return [a[0]/n,a[1]/n,a[2]/n]; }
    function cross3(a,b){ return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]; }
    function addMatrix(A,B){ for(let i=0;i<A.length;i++) for(let j=0;j<A[i].length;j++) A[i][j]+=B[i][j]; }
    function matVec(A,x){ return A.map(r=>r.reduce((s,v,j)=>s+v*x[j],0)); }

    function gaussianSolve(A,b){
        const n=A.length, M=A.map(r=>r.slice()), rhs=b.slice();
        let maxDiag=0; for(let i=0;i<n;i++) maxDiag=Math.max(maxDiag,Math.abs(M[i][i]));
        const tol=Math.max(1e-12,maxDiag*1e-12);
        for(let k=0;k<n;k++){
            let pivot=k, pv=Math.abs(M[k][k]);
            for(let i=k+1;i<n;i++){ const av=Math.abs(M[i][k]); if(av>pv){pv=av;pivot=i;} }
            if(pv<tol) throw new Error(`Singular/unstable stiffness matrix at DOF ${k+1}. Check supports or connectivity.`);
            if(pivot!==k){ [M[pivot],M[k]]=[M[k],M[pivot]]; [rhs[pivot],rhs[k]]=[rhs[k],rhs[pivot]]; }
            for(let i=k+1;i<n;i++){
                const f=M[i][k]/M[k][k];
                if(Math.abs(f)<1e-18) continue;
                M[i][k]=0;
                for(let j=k+1;j<n;j++) M[i][j]-=f*M[k][j];
                rhs[i]-=f*rhs[k];
            }
        }
        const x=Array(n).fill(0);
        for(let i=n-1;i>=0;i--){ let sum=rhs[i]; for(let j=i+1;j<n;j++) sum-=M[i][j]*x[j]; x[i]=sum/M[i][i]; }
        return x;
    }

    function frameLocalStiffness(E,G,A,Iy,Iz,J,L){
        const k=zeros(12,12), EA=E*A/L, GJ=G*J/L;
        const a=12*E*Iz/Math.pow(L,3), b=6*E*Iz/Math.pow(L,2), c=4*E*Iz/L, d=2*E*Iz/L;
        const e=12*E*Iy/Math.pow(L,3), f=6*E*Iy/Math.pow(L,2), g=4*E*Iy/L, h=2*E*Iy/L;
        k[0][0]=EA;k[0][6]=-EA;k[6][0]=-EA;k[6][6]=EA;
        k[3][3]=GJ;k[3][9]=-GJ;k[9][3]=-GJ;k[9][9]=GJ;
        const rz=[1,5,7,11];
        [[a,b,-a,b],[b,c,-b,d],[-a,-b,a,-b],[b,d,-b,c]].forEach((row,i)=>row.forEach((v,j)=>k[rz[i]][rz[j]]+=v));
        const ry=[2,4,8,10];
        [[e,-f,-e,-f],[-f,g,f,h],[-e,f,e,f],[-f,h,f,g]].forEach((row,i)=>row.forEach((v,j)=>k[ry[i]][ry[j]]+=v));
        return k;
    }

    function frameTransformation(p1,p2){
        const dx=[p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]], x=normalize3(dx);
        let ref=Math.abs(dot3(x,[0,1,0]))<0.90?[0,1,0]:[0,0,1];
        let z=normalize3(cross3(x,ref));
        let y=normalize3(cross3(z,x));
        const R=[x,y,z];
        const T=zeros(12,12);
        for(let block=0;block<4;block++) for(let i=0;i<3;i++) for(let j=0;j<3;j++) T[block*3+i][block*3+j]=R[i][j];
        return {T,R,x,y,z};
    }

    function transpose(A){ return A[0].map((_,j)=>A.map(r=>r[j])); }
    function matMul(A,B){ const C=zeros(A.length,B[0].length); for(let i=0;i<A.length;i++) for(let k=0;k<B.length;k++){ const v=A[i][k]; if(Math.abs(v)<1e-18) continue; for(let j=0;j<B[0].length;j++) C[i][j]+=v*B[k][j]; } return C; }

    function memberGlobalStiffness(elem,E,G,A,Iy,Iz,J){
        const p1=nodes[elem.nodes[0]],p2=nodes[elem.nodes[1]],L=Math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2+(p2[2]-p1[2])**2);
        const tr=frameTransformation(p1,p2), kl=frameLocalStiffness(E,G,A,Iy,Iz,J,L), kg=matMul(transpose(tr.T),matMul(kl,tr.T));
        return {kg,kl,T:tr.T,L,R:tr.R};
    }

    function addNodalForce(F,nodeId,fx,fy,fz){ const b=(nodeId-1)*6; F[b]+=fx;F[b+1]+=fy;F[b+2]+=fz; }

    function addUniformMemberLoad(F,elem,wGlobal){
        const p1=nodes[elem.nodes[0]],p2=nodes[elem.nodes[1]];
        const dx=[p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]], L=norm3(dx);
        const tr=frameTransformation(p1,p2), qx=dot3(wGlobal,tr.x), q=[dot3(wGlobal,tr.y),dot3(wGlobal,tr.z)];
        const fl=Array(12).fill(0);
        fl[0]+=qx*L/2; fl[6]+=qx*L/2;
        // Consistent nodal load for uniform transverse load in local y/z directions.
        fl[1]+=q[0]*L/2; fl[5]+=q[0]*L*L/12; fl[7]+=q[0]*L/2; fl[11]-=q[0]*L*L/12;
        fl[2]+=q[1]*L/2; fl[4]-=q[1]*L*L/12; fl[8]+=q[1]*L/2; fl[10]+=q[1]*L*L/12;
        const fg=matVec(transpose(tr.T),fl);
        const d0=(elem.nodes[0]-1)*6,d1=(elem.nodes[1]-1)*6;
        for(let i=0;i<6;i++){F[d0+i]+=fg[i];F[d1+i]+=fg[6+i];}
    }

    function buildLoadVector(lc,A,density){
        const n=Object.keys(nodes).length, F=Array(n*6).fill(0), def=getLoadDefinition(lc);
        const comp={Fx:0,Fy:0,Fz:0};
        const sw=def.selfWPerM;
        const addDistributedVertical=(elem,w)=>addUniformMemberLoad(F,elem,[0,-w,0]);
        if(def.factorD>0){
            if(lc==='LC1'||lc==='COMB1'||lc==='COMB2'||lc==='COMB_ASD1') elements.forEach(e=>addDistributedVertical(e,sw*def.factorD));
            if(lc!=='LC1') elements.filter(e=>e.type==='Roof Beam').forEach(e=>addDistributedVertical(e,5*def.factorD));
        }
        if(def.factorL>0){
            if(lc==='LC4'){
                const q=5*def.factorL/4; [5,6,7,8].forEach(id=>addNodalForce(F,id,0,-q,0));
            } else elements.filter(e=>e.type==='Roof Beam').forEach(e=>addDistributedVertical(e,3*def.factorL));
        }
        if(def.Fx){ const q=def.Fx/4; [5,6,7,8].forEach(id=>addNodalForce(F,id,q,0,0)); }
        if(def.Fz){ const q=def.Fz/4; [5,6,7,8].forEach(id=>addNodalForce(F,id,0,0,q)); }
        for(let i=0;i<n;i++){comp.Fx+=F[i*6];comp.Fy+=F[i*6+1];comp.Fz+=F[i*6+2];}
        comp.magnitude=Math.sqrt(comp.Fx**2+comp.Fy**2+comp.Fz**2);
        return {F,components:comp};
    }

    function solveMatrixFEM(){
        const lc=document.getElementById('active-loadcase').value;
        try{
            lastSolveError='';
            const Einput=parseFloat(document.getElementById('mat-e').value)||200000;
            const b=parseFloat(document.getElementById('sec-b').value)||300;
            const h=parseFloat(document.getElementById('sec-h').value)||450;
            const density=parseFloat(document.getElementById('mat-dens').value)||24;
            const A=isImperial?(b*h)/144:(b*h)/1e6;
            const E=isImperial?Einput*144:Einput*1000;
            const nu=0.20, G=E/(2*(1+nu));
            const Iy=isImperial?(b*Math.pow(h,3)/12)/20736:(b*Math.pow(h,3)/12)/1e12;
            const Iz=isImperial?(Math.pow(b,3)*h/12)/20736:(Math.pow(b,3)*h/12)/1e12;
            const J=Math.max(Iy+Iz,1e-14);
            const N=Object.keys(nodes).length, ndof=N*6, K=zeros(ndof,ndof);
            const memberCache={};
            elements.forEach(e=>{ const m=memberGlobalStiffness(e,E,G,A,Iy,Iz,J); memberCache[e.id]=m; const dofs=[]; [e.nodes[0],e.nodes[1]].forEach(n=>{const b0=(n-1)*6;for(let d=0;d<6;d++)dofs.push(b0+d);}); for(let i=0;i<12;i++)for(let j=0;j<12;j++)K[dofs[i]][dofs[j]]+=m.kg[i][j]; });
            const load=buildLoadVector(lc,A,density), F=load.F.slice();

            // Optional rigid-diaphragm penalty: equal roof Ux/Uz to master node.
            if(diaphragmEnabled){
                const roof=[5,6,7,8], master=5, diag=Math.max(...K.map((r,i)=>Math.abs(r[i])));
                const penalty=Math.max(diag*1e7,1e6);
                roof.filter(id=>id!==master).forEach(id=>{
                    const ux=(id-1)*6, uz=ux+2, mux=(master-1)*6, muz=mux+2;
                    [[ux,mux],[uz,muz]].forEach(([a,b])=>{K[a][a]+=penalty;K[b][b]+=penalty;K[a][b]-=penalty;K[b][a]-=penalty;});
                });
            }

            const fixed=[]; [1,2,3,4].forEach(nid=>{const b0=(nid-1)*6;for(let d=0;d<6;d++)fixed.push(b0+d);});
            const free=[]; for(let i=0;i<ndof;i++) if(!fixed.includes(i)) free.push(i);
            const Kff=free.map(i=>free.map(j=>K[i][j])), Ff=free.map(i=>F[i]);
            const Uf=gaussianSolve(Kff,Ff), U=Array(ndof).fill(0); free.forEach((d,i)=>U[d]=Uf[i]);
            const KU=matVec(K,U), R=KU.map((v,i)=>v-F[i]);

            computedResults.displacements={};
            computedResults.displacementModel={};
            for(let id=1;id<=N;id++){const b0=(id-1)*6; const scale=isImperial?1:1000; computedResults.displacements[id]=[U[b0]*scale,U[b0+1]*scale,U[b0+2]*scale]; computedResults.displacementModel[id]=[U[b0],U[b0+1],U[b0+2]];}
            computedResults.reactions={};
            fixed.forEach(d=>{const nid=Math.floor(d/6)+1, dof=d%6; if(!computedResults.reactions[nid])computedResults.reactions[nid]=[0,0,0]; if(dof<3)computedResults.reactions[nid][dof]=R[d];});

            computedResults.memberForces={}; computedResults.memberEndForces={}; computedResults.memberEndDisplacements={};
            elements.forEach(e=>{
                const m=memberCache[e.id], dofs=[]; [e.nodes[0],e.nodes[1]].forEach(n=>{const b0=(n-1)*6;for(let d=0;d<6;d++)dofs.push(b0+d);});
                const ug=dofs.map(d=>U[d]), ul=matVec(m.T,ug), fl=matVec(m.kl,ul);
                // Positive local axial force = tension, negative = compression.
                computedResults.memberForces[e.id]=fl[0];
                computedResults.memberEndForces[e.id]={i:fl.slice(0,6),j:fl.slice(6,12),length:m.L};
                computedResults.memberEndDisplacements[e.id]={i:ul.slice(0,6),j:ul.slice(6,12)};
            });
            computedResults.loadComponents=load.components;
            computedResults.totalAppliedForce=load.components.magnitude;
            computedResults.maxDeflection=Math.max(...Object.values(computedResults.displacements).map(d=>Math.sqrt(d[0]**2+d[1]**2+d[2]**2)));
            let sumRx=0,sumRy=0,sumRz=0; fixed.forEach(d=>{if(d%6===0)sumRx+=R[d];else if(d%6===1)sumRy+=R[d];else if(d%6===2)sumRz+=R[d];});
            computedResults.equilibriumError=Math.hypot(sumRx+load.components.Fx,sumRy+load.components.Fy,sumRz+load.components.Fz);
            updateAudit(lc,load.components,computedResults.equilibriumError);
            renderModel();
            switchBottomTab(document.querySelector('.bottom-tab.active')?.id?.replace('btab-','')||'displacements');
            document.getElementById('solver-status').innerText='Converged';
            document.getElementById('sb-status').innerText='Solver Status: Converged';
        }catch(err){
            lastSolveError=err.message||String(err);
            document.getElementById('solver-status').innerText='Error';
            document.getElementById('sb-status').innerText='Solver Status: Error';
            document.getElementById('audit-eq-error').innerText=lastSolveError;
            document.getElementById('audit-eq-error').style.color='#c62828';
            console.error('FEM solver error:',err);
        }
    }

    function updateAudit(lc,comp,eq){
        const fUnit=isImperial?'kip':'kN', dUnit=isImperial?'in':'mm';
        const pass=eq<1e-6*Math.max(1,comp.magnitude);
        document.getElementById('audit-lc-name').innerText=lc;
        document.getElementById('audit-total-load').innerText=`${comp.magnitude.toFixed(3)} ${fUnit}`;
        document.getElementById('audit-eq-error').innerText=`${eq.toExponential(2)} ${fUnit} (${pass?'Pass':'Check'})`;
        document.getElementById('audit-eq-error').style.color=pass?'#2E7D32':'#c62828';
        document.getElementById('max-def').innerText=`${computedResults.maxDeflection.toFixed(3)} ${dUnit}`;
        document.getElementById('dash-active-lc').innerText=lc;
        document.getElementById('dash-max-disp').innerText=`${computedResults.maxDeflection.toFixed(3)} ${dUnit}`;
        const vals=Object.values(computedResults.memberForces); const maxM=vals.length?Math.max(...vals.map(v=>Math.abs(v))):0;
        const card=document.getElementById('dash-max-force'); if(card) card.innerText=`${maxM.toFixed(2)} ${fUnit}`;
        const comps=document.getElementById('dash-load-components'); if(comps) comps.innerHTML=`ΣFx ${comp.Fx.toFixed(2)} · ΣFy ${comp.Fy.toFixed(2)} · ΣFz ${comp.Fz.toFixed(2)} ${fUnit}`;
    }

    // View Mode Switcher: 3D View vs Load View
    function switchViewMode(mode) {
        currentViewMode=mode;
        document.getElementById('tab-mode-3d').classList.toggle('active',mode==='3D');
        document.getElementById('tab-mode-load').classList.toggle('active',mode==='LOAD');
        scene.background=new THREE.Color(mode==='LOAD'?0xFAF7F9:0xFFFDFD);
        visibility.loads = mode==='LOAD' ? true : visibility.loads;
        document.getElementById('plot-legend').style.display=visibility.legend?'block':'none';
        renderModel();
    }

    // Ribbon Tab Switching
    function switchRibbonTab(tabName) {
        document.querySelectorAll('.ribbon-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.ribbon-panel').forEach(p => p.classList.remove('active'));

        const targetTab = Array.from(document.querySelectorAll('.ribbon-tab')).find(t => t.innerText.toLowerCase() === tabName);
        if (targetTab) targetTab.classList.add('active');

        const targetPanel = document.getElementById(`panel-${tabName}`);
        if (targetPanel) targetPanel.classList.add('active');

        if (tabName === 'home') {
            document.getElementById('home-dashboard-view').classList.add('active');
        } else {
            document.getElementById('home-dashboard-view').classList.remove('active');
        }
    }

    function toggleDashboardOverlay() {
        const el=document.getElementById('home-dashboard-view');
        el.classList.toggle('active');
        if(el.classList.contains('active')) switchRibbonTab('home');
    }

    // Bottom Table Tab Switching
    function switchBottomTab(tabKey) {
        const panel=document.getElementById('bottom-panel');
        if(panel && panel.classList.contains('collapsed')){ panel.classList.remove('collapsed'); setTimeout(()=>onResize(),50); }
        document.querySelectorAll('.bottom-tab').forEach(t => t.classList.remove('active'));
        const activeTab = document.getElementById(`btab-${tabKey}`);
        if (activeTab) activeTab.classList.add('active');

        const container = document.getElementById('bottom-table-container');
        const fUnit = isImperial ? 'kip' : 'kN';
        const dUnit = isImperial ? 'in' : 'mm';
        const lUnit = isImperial ? 'ft' : 'm';

        if (tabKey === 'displacements') {
            let rows = '';
            for (let id = 1; id <= 8; id++) {
                const [ux, uy, uz] = computedResults.displacements[id] || [0,0,0];
                const res = Math.sqrt(ux*ux + uy*uy + uz*uz);
                rows += `<tr><td>N${id}</td><td>${ux.toFixed(3)}</td><td>${uy.toFixed(3)}</td><td>${uz.toFixed(3)}</td><td><strong>${res.toFixed(3)}</strong></td></tr>`;
            }
            container.innerHTML = `
                <table class="eng-table">
                    <thead><tr><th>Node ID</th><th>UX [${dUnit}]</th><th>UY [${dUnit}]</th><th>UZ [${dUnit}]</th><th>Resultant [${dUnit}]</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            `;
        } else if (tabKey === 'reactions') {
            let rows = '';
            let sumFx = 0, sumFy = 0, sumFz = 0;
            for (let id = 1; id <= 4; id++) {
                const [fx, fy, fz] = computedResults.reactions[id] || [0,0,0];
                sumFx += fx; sumFy += fy; sumFz += fz;
                rows += `<tr><td>N${id} (Base)</td><td>${fx.toFixed(3)}</td><td>${fy.toFixed(3)}</td><td>${fz.toFixed(3)}</td></tr>`;
            }
            rows += `<tr style="font-weight:bold; background:var(--table-header-bg);"><td>Total Reaction Sum</td><td>${sumFx.toFixed(3)}</td><td>${sumFy.toFixed(3)}</td><td>${sumFz.toFixed(3)}</td></tr>`;
            container.innerHTML = `
                <table class="eng-table">
                    <thead><tr><th>Support Node</th><th>FX [${fUnit}]</th><th>FY [${fUnit}]</th><th>FZ [${fUnit}]</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            `;
        } else if (tabKey === 'member_forces') {
            let rows = '';
            elements.forEach(e => {
                const f = computedResults.memberForces[e.id] || 0;
                const ef = computedResults.memberEndForces[e.id] || {i:[0,0,0,0,0,0],j:[0,0,0,0,0,0]};
                const maxV=Math.max(Math.abs(ef.i[1]),Math.abs(ef.i[2]),Math.abs(ef.j[1]),Math.abs(ef.j[2]));
                const maxM=Math.max(Math.abs(ef.i[4]),Math.abs(ef.i[5]),Math.abs(ef.j[4]),Math.abs(ef.j[5]));
                const status = f < -0.01 ? 'Compression' : f > 0.01 ? 'Tension' : 'Near Zero';
                rows += `<tr><td>${e.id}</td><td>${e.type}</td><td>${f.toFixed(3)}</td><td>${maxV.toFixed(3)}</td><td>${maxM.toFixed(3)}</td><td>${status}</td></tr>`;
            });
            container.innerHTML = `
                <table class="eng-table">
                    <thead><tr><th>Member ID</th><th>Member Type</th><th>Axial [${fUnit}]</th><th>Max Shear [${fUnit}]</th><th>Max Moment [${isImperial?'kip-ft':'kN·m'}]</th><th>Status</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            `;
        } else if (tabKey === 'nodes') {
            let rows = '';
            Object.keys(nodes).forEach(id => {
                const [x, y, z] = nodes[id];
                rows += `<tr><td>N${id}</td><td>${x.toFixed(2)}</td><td>${y.toFixed(2)}</td><td>${z.toFixed(2)}</td><td>${y===0?'Fixed Base':'Free / Diaphragm'}</td></tr>`;
            });
            container.innerHTML = `<table class="eng-table"><thead><tr><th>Node ID</th><th>X [${lUnit}]</th><th>Y [${lUnit}]</th><th>Z [${lUnit}]</th><th>Boundary Condition</th></tr></thead><tbody>${rows}</tbody></table>`;
        } else if (tabKey === 'members') {
            let rows = '';
            const b = document.getElementById('sec-b').value;
            const h = document.getElementById('sec-h').value;
            elements.forEach(e => {
                rows += `<tr><td>${e.id}</td><td>N${e.nodes[0]}</td><td>N${e.nodes[1]}</td><td>${b}x${h} ${isImperial?'in':'mm'} Rect Beam</td></tr>`;
            });
            container.innerHTML = `<table class="eng-table"><thead><tr><th>Member ID</th><th>Start Node</th><th>End Node</th><th>Section Properties</th></tr></thead><tbody>${rows}</tbody></table>`;
        } else if (tabKey === 'audit') {
            const c=computedResults.loadComponents||{Fx:0,Fy:0,Fz:0,magnitude:0};
            const eq=computedResults.equilibriumError||0;
            container.innerHTML = `
                <div style="font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;color:var(--text-main);line-height:1.7;padding:10px;">
                    <div>[INFO] Global model: ${Object.keys(nodes).length} nodes × 6 DOF = ${Object.keys(nodes).length*6} DOF.</div>
                    <div>[INFO] Element formulation: 3D Euler-Bernoulli frame, 12 DOF/member.</div>
                    <div>[INFO] Fixed restraints: N1–N4, all translational and rotational DOF.</div>
                    <div>[INFO] Rigid diaphragm: <b>${diaphragmEnabled?'ENABLED':'OFF'}</b>${diaphragmEnabled?' (roof Ux/Uz coupled to N5)':''}.</div>
                    <div>[INFO] Active load case: <b>${document.getElementById('active-loadcase').value}</b>.</div>
                    <div>[INFO] Applied resultant: ${c.magnitude.toFixed(4)} ${fUnit}; ΣFx=${c.Fx.toFixed(4)}, ΣFy=${c.Fy.toFixed(4)}, ΣFz=${c.Fz.toFixed(4)} ${fUnit}.</div>
                    <div>[INFO] Linear system: Kff · U = Ff solved with partial-pivot Gaussian elimination.</div>
                    <div>[SUCCESS] Equilibrium residual at restraints: ${eq.toExponential(3)} ${fUnit}.</div>
                    ${lastSolveError?`<div style="color:#c62828">[ERROR] ${lastSolveError}</div>`:''}
                </div>`;
        }
    }

    // Toggle Left & Bottom Panels with Full Visibility Logic
    function toggleLeftPanel() {
        const lp = document.getElementById('left-panel');
        const expandBtn = document.getElementById('left-panel-expand-btn');
        lp.classList.toggle('collapsed');
        
        if (lp.classList.contains('collapsed')) {
            expandBtn.style.display = 'block';
        } else {
            expandBtn.style.display = 'none';
        }
        setTimeout(() => onResize(), 300);
    }

    function toggleBottomPanel() {
        document.getElementById('bottom-panel').classList.toggle('collapsed');
        setTimeout(() => onResize(), 300);
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-theme');
    }

    // Unit System Selector — converts geometry and material inputs rather than only relabeling them.
    function toggleUnits(){
        const target=document.getElementById('unit-system-select').value;
        const nextImperial=target==='IMP';
        if(nextImperial===isImperial) return;
        const Lconv=3.28083989501312, Econv=1/6.89475729317, densConv=0.0063658804, dimConv=1/25.4;
        const factor=nextImperial?Lconv:1/Lconv;
        Object.keys(nodes).forEach(id=>nodes[id]=nodes[id].map(v=>v*factor));
        cubeDim*=factor;
        const e=parseFloat(document.getElementById('mat-e').value)||200000;
        const dens=parseFloat(document.getElementById('mat-dens').value)||24;
        const b=parseFloat(document.getElementById('sec-b').value)||300;
        const h=parseFloat(document.getElementById('sec-h').value)||450;
        if(nextImperial){
            document.getElementById('mat-e').value=(e*Econv).toFixed(4);
            document.getElementById('mat-dens').value=(dens*densConv).toFixed(5);
            document.getElementById('sec-b').value=(b*25.4).toFixed(3);
            document.getElementById('sec-h').value=(h*25.4).toFixed(3);
        }else{
            document.getElementById('mat-e').value=(e*6.89475729317).toFixed(2);
            document.getElementById('mat-dens').value=(dens/0.0063658804).toFixed(3);
            document.getElementById('sec-b').value=(b/25.4).toFixed(2);
            document.getElementById('sec-h').value=(h/25.4).toFixed(2);
        }
        isImperial=nextImperial;
        document.getElementById('cube-dim-input').value=cubeDim.toFixed(3);
        document.getElementById('sb-unit').innerText=isImperial?'Unit: Imperial':'Unit: SI';
        document.getElementById('title-unit-display').innerText=isImperial?'Imperial (kip, ft, in, ksi)':'SI (kN, m, mm, MPa)';
        document.getElementById('lbl-diaphragm-elevation').innerText=isImperial?'Elevation [ft]:':'Elevation [m]:';
        document.getElementById('lbl-mat-e').innerText=isImperial?'E [ksi]:':'E [MPa]:';
        document.getElementById('lbl-mat-dens').innerText=isImperial?'Density [kip/ft³]:':'Density [kN/m³]:';
        document.getElementById('lbl-sec-b').innerText=isImperial?'Width b [in]:':'Width b [mm]:';
        document.getElementById('lbl-sec-h').innerText=isImperial?'Depth h [in]:':'Depth h [mm]:';
        controls.target.set(cubeDim/2,cubeDim/2,cubeDim/2);
        create3DGridPlanes();
        solveMatrixFEM(); switchBottomTab('displacements');
    }

    function updateLoadCaseView() {
        solveMatrixFEM();
    }

    function updateCubeDimensions(){
        const val=parseFloat(document.getElementById('cube-dim-input').value)||6;
        cubeDim=Math.max(.5,val);
        nodes[2][0]=cubeDim; nodes[3][0]=cubeDim; nodes[3][2]=cubeDim; nodes[4][2]=cubeDim;
        nodes[5][1]=cubeDim; nodes[6][0]=cubeDim; nodes[6][1]=cubeDim; nodes[7][0]=cubeDim; nodes[7][1]=cubeDim; nodes[7][2]=cubeDim; nodes[8][1]=cubeDim; nodes[8][2]=cubeDim;
        controls.target.set(cubeDim/2,cubeDim/2,cubeDim/2);
        create3DGridPlanes(); setCameraPreset('iso'); solveMatrixFEM();
    }

    function applyDiaphragmConstraint(){
        diaphragmEnabled=!diaphragmEnabled;
        const buttons=[...document.querySelectorAll('button')].filter(b=>b.innerText.includes('Apply Diaphragm'));
        buttons.forEach(b=>{b.innerText=diaphragmEnabled?'Remove Diaphragm':'Apply Diaphragm';});
        solveMatrixFEM();
        document.getElementById('sb-status').innerText=`Solver Status: ${diaphragmEnabled?'Diaphragm Enabled':'Converged'}`;
    }

    function runRev3Solver(){
        solveMatrixFEM();
        switchBottomTab('displacements');
    }

    function validateModel(){
        const errors=[];
        if(Object.keys(nodes).length<2) errors.push('At least two nodes are required.');
        elements.forEach(e=>{ if(!nodes[e.nodes[0]]||!nodes[e.nodes[1]]) errors.push(`${e.id}: invalid node reference.`); });
        const E=parseFloat(document.getElementById('mat-e').value), b=parseFloat(document.getElementById('sec-b').value), h=parseFloat(document.getElementById('sec-h').value);
        if(!(E>0)) errors.push('Elastic modulus E must be positive.');
        if(!(b>0&&h>0)) errors.push('Section dimensions must be positive.');
        const lengths=elements.map(e=>{const a=nodes[e.nodes[0]],b0=nodes[e.nodes[1]];return Math.hypot(b0[0]-a[0],b0[1]-a[1],b0[2]-a[2]);});
        if(lengths.some(L=>L<1e-9)) errors.push('Zero-length member detected.');
        if(errors.length){ alert('MODEL VALIDATION\\n\\n'+errors.join('\\n')); return false; }
        alert(`MODEL VALIDATION PASSED\\n\\nNodes: ${Object.keys(nodes).length}\\nMembers: ${elements.length}\\nFixed supports: 4\\nLoad case: ${document.getElementById('active-loadcase').value}\\nDiaphragm: ${diaphragmEnabled?'Enabled':'Off'}`);
        return true;
    }

    function setCameraPreset(preset){
        const c=cubeDim/2, r=Math.max(cubeDim*2.4,12);
        if(preset==='iso') camera.position.set(c+r*.82,c+r*.62,c+r*.92);
        else if(preset==='top') camera.position.set(c,c+r,c+.01);
        else if(preset==='front') camera.position.set(c,c,c+r);
        else if(preset==='right') camera.position.set(c+r,c,c);
        controls.target.set(c,c,c); controls.update();
    }
    function resetCameraView(){setCameraPreset('iso');}

    function toggleVisibility(item){ visibility[item]=!visibility[item]; renderModel(); }
    function setDisplayOption(key,value){ displayOptions[key]=!!value; renderModel(); }
    function toggleDisplayOption(key){ setDisplayOption(key,!displayOptions[key]); const el=document.getElementById('chk-force-labels'); if(key==='forceLabels'&&el)el.checked=displayOptions[key]; const ov=document.getElementById('chk-deformed-overlay'); if(key==='deformedOverlay'&&ov)ov.checked=displayOptions[key]; }
    function setForceScale(v){forceScale=parseFloat(v)||1;document.getElementById('force-scale-value').innerText=forceScale.toFixed(1)+'×';renderModel();}
    function setDeformScale(v){deformScale=parseFloat(v)||20;document.getElementById('deform-scale-value').innerText=deformScale.toFixed(0)+'×';renderModel();}
    function setLabelScale(v){
        labelScale=Math.max(0.5,Math.min(3.0,parseFloat(v)||1));
        document.getElementById('label-scale-value').innerText=labelScale.toFixed(2)+'×';
        renderModel();
    }
    function setDiagramScale(v){ diagramScale=Math.max(.15,Math.min(1,parseFloat(v)||.35)); const e=document.getElementById('diagram-scale-value'); if(e)e.innerText=diagramScale.toFixed(2)+'×'; renderModel(); }
    function setResultDiagram(mode){ resultDiagramMode=mode||'none'; const a=document.getElementById('result-diagram-select');if(a)a.value=resultDiagramMode; const b=document.getElementById('result-diagram-inline');if(b)b.value=resultDiagramMode; renderModel(); }
    function toggleReferencePlanes(){ referencePlanesVisible=!referencePlanesVisible; create3DGridPlanes(); const b=document.getElementById('reference-plane-badge');if(b)b.style.display=referencePlanesVisible?'block':'none'; }

    function newProject(){
        document.getElementById('proj-name').value='New Cube Frame Model';
        document.getElementById('cube-dim-input').value='6.0';
        document.getElementById('mat-e').value=isImperial?'29':'200000';
        document.getElementById('mat-dens').value=isImperial?'0.150':'24.0';
        document.getElementById('sec-b').value=isImperial?'12':'300';
        document.getElementById('sec-h').value=isImperial?'18':'450';
        cubeDim=6; updateCubeDimensions();
        document.getElementById('save-indicator').innerText='New';
    }

    function serializeProject(){
        return {version:'Cube FEM Studio Rev 7 Phase 2',projectName:document.getElementById('proj-name').value,cubeDim,nodes,elements,material:{E:document.getElementById('mat-e').value,density:document.getElementById('mat-dens').value,b:document.getElementById('sec-b').value,h:document.getElementById('sec-h').value},activeLoadCase:document.getElementById('active-loadcase').value,diaphragmEnabled,labelScale};
    }
    function saveProject(){
        const blob=new Blob([JSON.stringify(serializeProject(),null,2)],{type:'application/json'});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=(document.getElementById('proj-name').value||'Cube_FEM_Model')+'.json'; a.click(); URL.revokeObjectURL(a.href);
        document.getElementById('save-indicator').innerText='Saved';
    }
    function openProjectPicker(){ document.getElementById('project-file-input').click(); }
    function loadProjectFile(event){
        const file=event.target.files?.[0]; if(!file) return;
        const reader=new FileReader();
        reader.onload=()=>{
            try{
                const d=JSON.parse(reader.result);
                if(d.cubeDim) document.getElementById('cube-dim-input').value=d.cubeDim;
                if(d.projectName) document.getElementById('proj-name').value=d.projectName;
                if(d.material){ if(d.material.E!=null)document.getElementById('mat-e').value=d.material.E; if(d.material.density!=null)document.getElementById('mat-dens').value=d.material.density; if(d.material.b!=null)document.getElementById('sec-b').value=d.material.b; if(d.material.h!=null)document.getElementById('sec-h').value=d.material.h; }
                if(d.nodes) nodes=d.nodes; if(d.elements) elements=d.elements; if(d.diaphragmEnabled!=null)diaphragmEnabled=!!d.diaphragmEnabled;
                if(d.activeLoadCase) document.getElementById('active-loadcase').value=d.activeLoadCase;
                cubeDim=parseFloat(document.getElementById('cube-dim-input').value)||6;
                document.getElementById('save-indicator').innerText='Loaded'; solveMatrixFEM();
            }catch(e){ alert('Unable to open project file: '+e.message); }
            event.target.value='';
        };
        reader.readAsText(file);
    }
    function showAbout(){ alert('Cube FEM Studio Rev 7\\n\\n3D structural frame solver with a true 6-DOF/node matrix stiffness engine, active load-case visualization, force diagrams, result tables, model validation, and JSON/CSV export.'); }

    // CSV / Excel Export Function
    function exportToExcelCSV(){
        const lc=document.getElementById('active-loadcase').value, fUnit=isImperial?'kip':'kN', dUnit=isImperial?'in':'mm', mUnit=isImperial?'kip-ft':'kN·m';
        const c=computedResults.loadComponents||{Fx:0,Fy:0,Fz:0,magnitude:0};
        const rows=[];
        const push=(...v)=>rows.push(v.map(x=>`"${String(x).replace(/"/g,'""')}"`).join(','));
        push('CUBE FEM STUDIO - STRUCTURAL ANALYSIS REPORT');
        push('Active Load Case',lc); push('Total Applied Resultant ['+fUnit+']',computedResults.totalAppliedForce.toFixed(6));
        push('Sigma Fx ['+fUnit+']',c.Fx.toFixed(6)); push('Sigma Fy ['+fUnit+']',c.Fy.toFixed(6)); push('Sigma Fz ['+fUnit+']',c.Fz.toFixed(6));
        push('Max Deflection ['+dUnit+']',computedResults.maxDeflection.toFixed(6)); push('Equilibrium Residual ['+fUnit+']',computedResults.equilibriumError.toExponential(6));
        rows.push(''); push('NODAL DISPLACEMENTS'); push('Node ID','UX ['+dUnit+']','UY ['+dUnit+']','UZ ['+dUnit+']','Resultant ['+dUnit+']');
        Object.keys(nodes).forEach(id=>{const d=computedResults.displacements[id]||[0,0,0];push('N'+id,d[0].toFixed(6),d[1].toFixed(6),d[2].toFixed(6),Math.hypot(...d).toFixed(6));});
        rows.push(''); push('SUPPORT REACTIONS'); push('Node','FX ['+fUnit+']','FY ['+fUnit+']','FZ ['+fUnit+']');
        Object.keys(computedResults.reactions||{}).forEach(id=>{const r=computedResults.reactions[id];push('N'+id,r[0].toFixed(6),r[1].toFixed(6),r[2].toFixed(6));});
        rows.push(''); push('MEMBER FORCES'); push('Member','Type','Axial ['+fUnit+']','Max Shear ['+fUnit+']','Max Moment ['+mUnit+']','Status');
        elements.forEach(e=>{const f=computedResults.memberForces[e.id]||0,ef=computedResults.memberEndForces[e.id]||{i:[0,0,0,0,0,0],j:[0,0,0,0,0,0]};const v=Math.max(Math.abs(ef.i[1]),Math.abs(ef.i[2]),Math.abs(ef.j[1]),Math.abs(ef.j[2]));const m=Math.max(Math.abs(ef.i[4]),Math.abs(ef.i[5]),Math.abs(ef.j[4]),Math.abs(ef.j[5]));push(e.id,e.type,f.toFixed(6),v.toFixed(6),m.toFixed(6),f<-0.01?'Compression':f>0.01?'Tension':'Near Zero');});
        const blob=new Blob([rows.join('\\n')],{type:'text/csv;charset=utf-8'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=`Cube_FEM_Results_${lc}.csv`; a.click(); URL.revokeObjectURL(a.href);
    }

    function onResize() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }

    window.addEventListener('resize', onResize);

    // Initial Execution
    const refBadge=document.getElementById('reference-plane-badge'); if(refBadge)refBadge.style.display=referencePlanesVisible?'block':'none';
    setResultDiagram('none');
    solveMatrixFEM();
    switchBottomTab('displacements');

    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
</script>
</body>
</html>
"""
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    abs_path = os.path.abspath(output_filename)
    print(
        "Cube FEM Studio Interactive Dashboard generated successfully at:"
        f" {abs_path}"
    )

    try:
        webbrowser.open(f"file://{abs_path}")
    except Exception as e:
        print(f"File created. Open manually in web browser: {e}")


if __name__ == "__main__":
    generate_interactive_ui("app.html")