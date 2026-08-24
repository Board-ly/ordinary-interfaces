# Interface Copy

9 rules. Words in an interface are design material, a label carries as much of
the hierarchy as its type size does.

**Clear beats clever; consistent beats varied. The best error message is the
interaction redesigned so the error cannot happen.**

**Before writing or reviewing, read the copy nearby.** Note the product's
terminology, its localisation conventions, and any voice guide. A deliberate
brand voice is not a defect. Raise a departure from plain language only when it
creates inconsistency, ambiguity, translation risk, or a tone the stakes will not
support.

---

## `voice-and-tone`: One Voice, Tone Flexes With Stakes · high

> The product has one voice, established by its existing copy. A local edit does
> not get to invent a new one.

| Context | Tone |
|---|---|
| Success, onboarding, empty states | warm, can be light |
| Routine actions, settings | neutral, minimal |
| Errors, destructive confirmations | calm, plain, **zero playfulness** |
| Data loss, security | serious, explicit |

**Address the reader directly.** "you", not "the user". In errors, "we" invites
ambiguity and reads as deflection: **"Unable to load content"** beats "We're
having trouble loading this content". Use possessives sparingly, "Favorites"
beats "Your Favorites". Hold one perspective through a whole flow.

**Plain words over clever ones.** Choose words a tired reader gets on the first
pass and delete every word doing no work. No idioms, no colloquialisms, no humour
that will not translate. Skip unnecessary gender. **Match the input device**,
"tap" on touch, "click" with a pointer, "select" when both are possible.

---

## `consistent-vocabulary`: One Noun, One Verb, Per Concept · high

> If the empty state says "projects", the summary says "workspaces" and the
> button says "boards", the product has three mental models.

**One noun per concept**, enforced across every state, tab and toast. **One verb
per action**, "Connect calendar" and "Sync calendar" are two features to a user
and one button in the code.

**Consistent flow vocabulary.** A multi-step flow uses one set: "Get started" to
enter, "Continue" *or* "Next" (pick one) to advance, "Done" to finish.
**Alternating synonyms makes users wonder whether the buttons do different
things**, which is a reasonable thing to wonder.

---

## `verb-first-buttons`: Start With the Verb · high

> "Send", "Save draft", "Delete project". Never "OK!", "Let's go!", or a bare
> "Yes" on a consequential action.

**A confirmation button repeats the consequence**, so the dialog is answerable
without reading the body:

> **Delete this project?** → `Delete project` · `Cancel`

**Why it holds.** People scan dialogs to the buttons. A button that names its own
outcome survives that scan; "Yes" requires reading back up, and under time
pressure it frequently does not get read.

---

## `link-text`: Make Sense Out of Context · high

> Screen reader users navigate by a list of the page's links, stripped of
> surrounding prose.

- "Read the billing docs", not "click here", which fails this *and* the device-verb rule at once.
- **A bare "Learn more" collapses the moment two appear on one page.** Suffix each: "Learn more about exports".

Satisfies SC 2.4.4 (`interaction.md → wcag-navigation`).

---

## `error-copy`: Say How to Fix It, Where It Broke · high

> An error is an instruction, and it belongs beside the field that failed.

| Instead of | Write |
|---|---|
| That password is too short | **Choose a password with at least 8 characters** |
| Invalid name | **Use only letters for your name** |
| Oops! Something went wrong. | **Unable to save. Check your connection and try again.** |

- **No blame, no "oops", no exclamation marks.**
- **Phrase hints positively.** "Use only letters", not "Don't use numbers or symbols".
- **Show the hint before the mistake**, not after.
- **Name the object precisely.** A phone number is not an address.
- **When the same error keeps firing, redesign the interaction rather than rewording it.**

Placement and taxonomy: `states.md → error-taxonomy`. Announcement:
`a11y-implementation.md → error-announcement`.

---

## `empty-state-copy`: Orientation Plus a Next Step · high

> Say what this place is, how to fill it, and offer one clear action.

```html
<!-- Bad: a shrug -->
<p>No results.</p>

<!-- Good -->
<p class="font-medium">No projects yet</p>
<p class="text-sm text-muted">Projects keep your tasks and files together.</p>
<button class="mt-4">Create a project</button>
```

**Lead with the benefit, not the mechanism.** "Tells you the moment a build
breaks" beats "Enables webhook event ingestion".

**A search or filter empty state names the query and offers the exit:** "No
results for 'quarterly'. Clear filters."

**Never park persistent information in an empty state.** It disappears the
moment content exists, which is precisely when people go looking for it.

Which of the three empty states you are writing: `states.md → empty-states`.

---

## `toggle-labels`: Describe the ON State · medium

> "Send read receipts", not "Don't send read receipts".

Labelling the negative turns the toggle into a double negative, off means don't
don't send, and readers reliably get it wrong under any time pressure. Labelling
the on state lets the off state be inferred.

**Link straight to a referenced setting** rather than describing the path: a
"Notification settings" link, not "Go to Settings > Notifications > Email".

---

## `capitalization-policy`: One Policy Per Element Type · medium

> Pick title case or sentence case per element type, then apply it to every
> instance of that type.

**Sentence case is the safer default.** Calmer, no per-word rules to remember,
and it localises cleanly. "Save Changes" beside "Discard changes" reads as
carelessness rather than as two decisions.

Store text in natural case and apply presentation with `text-transform`
(`typography.md → smart-punctuation`).

---

## `no-string-concatenation`: Never Assemble a Sentence · high

```js
// Bad, word order changes per language
"You have " + n + " new messages"
```

**Use a full templated string with proper pluralisation.** Concatenating around a
variable produces broken grammar in most languages that are not English, and it
is invisible until someone translates it, at which point it is scattered across
the codebase.

**Placeholders are examples, not labels.** A placeholder shows expected format,
`name@example.com`, `DD/MM/YYYY`, and **vanishes on input**, so it is never the
only label. Every field keeps a visible one
(`a11y-implementation.md → form-controls`).
