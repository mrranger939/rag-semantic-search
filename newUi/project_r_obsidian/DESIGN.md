# Design System Specification: Project R

## 1. Overview & Creative North Star
**Creative North Star: "The Synthetic Architect"**

The design system is engineered to move beyond the "SaaS Template" aesthetic. It embraces an editorial, high-tech philosophy where information isn't just displayed—it is curated. By utilizing a "Strict Dark" environment, we minimize ocular strain and maximize the vibrance of our intelligence layer (Electric Cyan).

The system breaks the traditional rigid grid through **Intentional Asymmetry** and **Tonal Depth**. We eschew the heavy-handed use of lines in favor of sophisticated layering, creating a UI that feels like a high-end physical console—precise, authoritative, and deeply immersive.

---

## 2. Colors & Surface Philosophy
The palette is rooted in deep blacks and cool grays to provide a void-like canvas where data can truly shine.

### The Color Tokens
*   **Background (`#131313` / `#0A0A0A`):** The foundation. Absolute blacks are reserved for the lowest level of the interface.
*   **Primary (`#00D2FF` / `primary_container`):** Our "Electric Cyan." This is used sparingly to signify intelligence, activity, and action.
*   **Surface Tiers:**
    *   `surface_container_lowest`: `#0E0E0E` (Deepest immersion)
    *   `surface_container_low`: `#1C1B1B` (Standard sectioning)
    *   `surface_container_high`: `#2A2A2A` (Active elevation)

### The "No-Line" Rule
**Strict Mandate:** Designers are prohibited from using 1px solid borders to define sections. Boundaries must be established through background color shifts or negative space. 
*   *Example:* A sidebar (`surface_container_low`) sits flush against the main dashboard (`background`) without a stroke. The 4-8% difference in luminance is the only required separator.

### Glass & Gradient Implementation
To achieve a "Signature" look, main CTAs should not be flat. Use a linear gradient: `primary` (#a5e7ff) to `primary_container` (#00D2FF) at a 135-degree angle. This provides a "liquid light" effect characteristic of high-end hardware.

---

## 3. Typography
We use a dual-typeface system to balance technical precision with editorial authority.

*   **Display & Headlines (Manrope):** Chosen for its geometric purity. Use `display-lg` (3.5rem) for high-impact data points. The wide tracking and modern curves project a sense of "The Future of Enterprise."
*   **Body & Labels (Inter):** The workhorse. Inter provides maximum legibility at small scales. Use `body-md` (0.875rem) for standard text to maintain a sophisticated, "small-print" technical feel.
*   **Hierarchy Note:** Always lead with high contrast. Use `on_surface` (white/light grey) for headlines and `on_surface_variant` (muted cyan-grey) for secondary descriptions to create an immediate visual path for the eye.

---

## 4. Elevation & Depth
In this design system, depth is a function of light, not structure.

### The Layering Principle
Think of the UI as stacked sheets of tinted glass. 
1.  **Level 0:** `surface_container_lowest` (The base floor).
2.  **Level 1:** `surface_container_low` (Sidebars and navigation).
3.  **Level 2:** `surface_container_high` (Cards and floating panels).

### Ambient Shadows & Ghost Borders
*   **Shadows:** Shadows must be invisible until noticed. Use a blur of 32px-64px with an opacity of 6% using a tinted shadow color derived from `primary` to simulate the glow of the screen.
*   **Ghost Borders:** If a separation is required for accessibility, use `outline_variant` at **15% opacity**. This creates a "glint" on the edge of a container rather than a visible cage.

---

## 5. Components

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary_container`), `DEFAULT` (8px) corners. No border. White text (`on_primary`).
*   **Secondary:** No fill. `Ghost Border` (15% opacity `outline`). Text in `primary_fixed_dim`.
*   **State:** Hovering a primary button should increase the `surface_tint` intensity, making the button appear to "charge" with light.

### Cards & Data Lists
*   **No Dividers:** Lists should use `spacing-4` (1rem) of vertical white space or a subtle `surface` shift on hover to separate items. 
*   **Nesting:** Place a `surface_container_highest` card inside a `surface_container_low` section to create "Natural Lift."

### Input Fields
*   **Style:** Minimalist. Use `surface_container_lowest` as the fill. 
*   **Active State:** The bottom edge glows with a 2px `primary` line, while the rest of the container remains borderless.

### AI Specialized Components
*   **The Intelligence Pulse:** For AI processing states, use a semi-transparent `primary` glow behind a `surface_container` with a `backdrop-blur` of 12px.
*   **Data Chips:** Small, `md` rounded (0.75rem) tags using `secondary_container` with `label-sm` typography.

---

## 6. Do’s and Don’ts

### Do
*   **Do** use extreme white space. Let the OLED black "breathe."
*   **Do** use `primary` (Electric Cyan) as a surgical tool. If everything is cyan, nothing is important.
*   **Do** use asymmetrical layouts (e.g., a wide left column for data and a narrow right column for meta-information).

### Don't
*   **Don’t** use pure white (#FFFFFF) for body text; use `on_surface` (#e5e2e1) to avoid "halo" effects on dark backgrounds.
*   **Don’t** use traditional 1px dividers. If you feel the need for a line, try a background color change first.
*   **Don’t** use standard "Drop Shadows." Use the soft, ambient glow method described in Section 4.