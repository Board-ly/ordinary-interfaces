# Accessibility in Practice

9 rules. `accessibility.md` is the WCAG cross-index; this is how you build it.

**Most accessibility is free if you use the platform.** Native elements ship with
keyboard support, real labels announce themselves, and a visible focus ring is
one CSS rule. When unsure, take the platform default over a custom rebuild, and
**remove ARIA rather than add it**.

Reviewing means two passes: **keyboard-only**, where every flow completes without
a mouse, then **screen-reader**, where every control announces a name, a role and
its state.

---

## `native-elements-first`: Don't Rebuild What Ships · **critical**

> The first rule of ARIA is not to use ARIA when a native element exists.

- `<button>` for actions, `<a href>` for navigation. **Never `<div onClick>`.**
- A real link supports Cmd/Ctrl/middle-click; an `<a>` without `href` does not, and does not appear in a screen reader's links list.
- **No ARIA is better than bad ARIA.** An incorrect role actively misdescribes the element, where a missing one merely under-describes it.

SC references (2.1.1, 4.1.2) in `accessibility.md → Code-level checks`.

---

## `focus-visible`: Style the Right Pseudo-Class · **critical**

> `:focus-visible`, not bare `:focus`. Prefer the browser's own indicator.

**Why it holds.** `:focus-visible` carries the browser's heuristic for whether
focus arrived by keyboard or by pointer, keyboard users get a ring, mouse users
usually do not. That heuristic is better maintained than one you would write, and
it is free.

**If you must customise:** a project focus token or an explicit color, verified
**against every adjacent color it crosses, `currentColor` included**. At least a
**2px solid perimeter** or equivalent visible area. **Never `outline: none`
without a verified replacement.** Preserve system colors in forced-colors mode.

Ring geometry and the 3:1 requirement (SC 2.4.11):
`interaction.md → button-design`.

---

## `keyboard-patterns`: Follow the APG · **critical**

| Key | Behaviour |
|---|---|
| Escape | closes overlays |
| Arrow keys | move **within** a composite widget |
| Tab | moves **between** widgets |
| Enter / Space | activate |

**`tabindex` takes exactly two values.** `0` joins the natural tab order; `-1`
allows programmatic focus. **Positive values override document order** and are
almost always a bug (SC 2.4.3), they also compound, since one positive value
pushes every natural element behind it.

**Composite widgets use roving tabindex.** The active item at `0`, every other
at `-1`.

---

## `focus-trap`: Trap on Open, Restore on Close · high

1. Set **`inert`** on the background content.
2. **Move focus inside** on open.
3. **Return focus to the trigger** on close.
4. **`overscroll-behavior: contain`** so the background does not scroll.

**Step 3 is the one that gets skipped**, and skipping it drops a keyboard user at
the top of the document with no indication of where they were.

---

## `hit-area-extension`: Grow the Target, Not the Glyph · high

**The spacing exception, stated precisely.** An undersized target passes when a
24px circle centred on its bounding box intersects no other target and no other
undersized target's circle. Concretely: **20px targets need a 4px gap**. Smaller
controls are not automatic failures, check the spacing, equivalent-control,
inline, user-agent and essential exceptions before reporting one.

**Extend with a pseudo-element**, on the wrapping `<label>` or `<button>`,
**never on the `<input>`**, because replaced elements do not render
`::before`/`::after` reliably.

```css
.checkbox-label { position: relative; width: 20px; height: 20px; }
.checkbox-label::after {
  content: ""; position: absolute;
  top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 44px; height: 44px;
}
```

**Two collision rules.** Never let extended hit areas overlap, an invisible 44px
box around a 20px control will eat its neighbour. And give decorative layers
`pointer-events: none`, so a glow or gradient never swallows clicks meant for the
control beneath.

**Anything that looks clickable is clickable across its whole visual extent**.
No dead zones. A checkbox and its label share one target.

Sizes and standards: `interaction.md → touch-target`.

---

## `form-controls`: Label, Type, and Never Block Paste · high

- Every input gets a `<label for>` or a wrapping `<label>`. **A placeholder is never a label.**
- **Label and control share one hit target**, with no dead zone between a checkbox and its text.
- Add **`autocomplete`** with a meaningful `name`, plus the **`type`** and **`inputmode`** that summon the right keyboard.
- **Never block paste.** People paste passwords and one-time codes; blocking it breaks password managers and undermines SC 3.3.8.

---

## `error-announcement`: Enabled Until Submitted · high

- **Keep submit enabled until the request starts**, then disable with a spinner and the original label. A submit disabled until the form is valid gives the user nothing to press and no explanation of why.
- **Validate on submit.**
- Mark failing fields **`aria-invalid="true"`**, point **`aria-describedby`** at the inline error, and **focus the first invalid field**.
- Use native **`disabled`** when a control is genuinely unavailable; reach for **`aria-disabled="true"`** only when it must stay focusable, then block pointer, keyboard and form behaviour in code and style the state explicitly.
- **A tooltip on a natively `disabled` control is unreachable.** Put the text beside it, or use `aria-disabled`.

---

## `live-regions`: Three Mechanisms, Three Jobs · high

| Mechanism | Carries |
|---|---|
| `aria-describedby` | field-specific validation, tied to a control |
| `role="status"` (polite) | non-urgent updates not tied to a control, toasts, result counts |
| `role="alert"` (assertive) | urgent untied errors, **and nothing else** |

**Repeated polite announcements need a stable empty region rendered before its
text updates.** Injecting the region and its content together is why the second
toast frequently goes unannounced, the region was not there to be watched.

**Dynamically inserted alerts vary in support**; test on the screen readers you
actually target. An `assertive` region for a routine toast interrupts whatever
the user was reading.

---

## `alt-by-purpose`: Describe the Job, Not the Picture · **critical**

| Image kind | Alt |
|---|---|
| Decorative | `alt=""` |
| Informative | the **meaning** |
| **Functional** | the **action** |

**A search icon button is `alt="Search"`, not `alt="magnifying glass"`.** The
alternative serves the equivalent *purpose*; for a control, the purpose is what
pressing it does.

Icon-only buttons need a descriptive `aria-label`. **Visible label text must
appear in the accessible name.** Decorative elements get `aria-hidden="true"`,
**never on a focusable element**, which would remove it from the accessibility
tree while leaving it in the tab order.

Full SC 1.1.1 treatment: `interaction.md → wcag-images`.

---

## Page structure and zoom

**Structure is navigation.** Headings describe their sections and form a coherent
outline: one `<h1>`, levels nested without skipping. Expose one visible primary
`<main>` landmark, and where repeated navigation precedes it, make a **"Skip to
content" link the first focusable element**. Anchored headings get
`scroll-margin-top`.

**Survive zoom.** The page works at **200%** and reflows at **320px** without
horizontal scrolling. **`min-height`, never fixed `height`**, on text containers.
Prefer `rem` breakpoints where they fit the codebase, and **never let the
viewport meta cap how far the reader can zoom.**

**Reduced motion**, extending `motion.md → reduced-motion`: wrap motion in
`@media (prefers-reduced-motion: no-preference)` so it is **opt-in**. Under
reduced motion, replace slides and scales with opacity crossfades and drop
parallax and autoplay entirely. Two rules hold **regardless** of the preference:
autoplaying media needs a visible pause control, and toasts carrying an action or
an error stay until dismissed.
