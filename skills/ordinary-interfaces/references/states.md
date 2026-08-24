# Non-Happy States

10 rules. A screen is a state machine with one photogenic state. That state gets
designed, gets built and ships; the rest get discovered by users.

---

## `state-ledger`: Decide Every State, in Writing · high

> A missing state and a state you decided against look identical in a codebase.
> The difference is that one was a decision.

**The rule.** No surface is done until every state it can enter has been designed
or explicitly ruled out **in writing**.

```
### Project list
source: GET /projects (cached, may be stale)

  [x] populated        | designed, built
  [x] empty:first-run  | designed, built
  [ ] empty:cleared    | MISSING
  [x] loading          | skeleton, 3 rows
  [ ] partial          | MISSING: projects with no thumbnail
  [x] error:transient  | inline retry
  [ ] error:terminal   | MISSING
  [x] offline/stale    | timestamp in header
  [ ] overflow         | MISSING: untested past 40 items
  [x] end-of-list      | n/a, infinite scroll, no terminus
```

Every row is `designed`, `MISSING`, or `n/a (<reason>)`. Blank is not an option,
and **`n/a` needs a reason**. A bare "n/a" is how a missing state disguises
itself as a decision.

**Order of work.** Ledger first. Then **build the hardest state first.** The
error, the 500-item list, the 47-character name. A layout that survives its worst
state survives its best one; the reverse is not true. Render against hostile
fixtures from the first commit, not at QA. Copy last.

**The four to ship regardless of budget.** Each under an hour, and together most
of the perceived gap between finished and unfinished:

1. **`empty:filtered`** on any surface with search or filter, the highest damage per hour of any state.
2. **Error with preserved input** on anything with a form.
3. **Loading with a delay guard** on the primary fetch.
4. **Overflow on the longest user-supplied string.** Find it, triple it, fix what breaks.

**Legitimate reasons to skip.** The state is unreachable (a static local array
has no loading state). A page-level boundary already owns it, one owner per
state per region. The case is impossible by construction (a drawer that only
opens when non-empty). Ceremony exceeds the event (a three-item settings list
needs no skeleton). **Skipping is fine; silence is not.**

---

## `empty-states`: Empty Is Three States · high

> All three render zero rows, which is why they get one screen, and that screen
> is wrong for two of them.

| | Meaning | Copy leads with | Primary action |
|---|---|---|---|
| **first-run** | no data has ever existed | what this will do for them | create / connect / import |
| **cleared** | data existed, the user removed it | acknowledgement, not celebration | create again, quietly |
| **filtered-to-zero** | data exists, the query hides it | what was searched, how many exist | **clear filters** |

**The failure that matters.** Showing "Create your first project" to someone with
forty projects who mistyped a search. **It tells them their data is gone.**
`filtered-to-zero` always names the filter and offers to remove it, and never
offers creation as the primary action.

**`cleared` is the one nobody builds.** Someone who just deleted everything does
not want confetti and an onboarding illustration. A calm surface and an
unobtrusive way back.

**Anatomy.** One line of what goes here, one line of why it is worth it, not a
paragraph. **Exactly one primary action**; two equal-weight cards is not a choice,
it is a stall, so rank them into one button and one text link. **No illustration
larger than the action it accompanies**, if the artwork outweighs the button,
the state is decoration. Never restate the actions in prose beneath the actions.

---

## `loading-strategy`: Choose by Layout Knowability · high

> Not by taste, and not by what the component library ships.

| Use | When |
|---|---|
| **Nothing** | expected **under 200ms.** A loader that flashes is worse than a beat of stillness |
| **Skeleton** | the final layout is knowable **before** the data arrives |
| **Spinner** | layout unknowable, region under **~120px**, or duration unbounded |
| **Optimistic** | the write is reversible, local-first and near-certain |

**Two guards separate polished from twitchy.**

- **Delay guard ~250ms.** Do not show the loader until 250ms has passed. Most requests resolve first and the user sees nothing at all.
- **Minimum display ~400ms.** Once shown, hold it, or a fast response produces a strobe.

**The skeleton condition is not optional.** A skeleton whose geometry does not
match the real content causes layout shift on resolve, **which is worse than a
spinner**. If you cannot match the geometry, you did not know the layout, so use
a spinner.

**Skeletons set `aria-busy` and announce completion.** A screen reader user
hearing nothing for four seconds does not know the app is working.

**Optimistic UI requires a rollback path and a visible failure surface.**
Optimistic UI without a failure surface is a lie.

---

## `partial-data`: Real Records Have Holes · high

> Null fields, 404 images, no avatar, a blank optional bio. All of these render.

- **Never render `undefined`, `null`, `NaN`, `Invalid Date`, or a bare `-`** where a value goes.
- **A missing image must not collapse the layout.** Reserve the box with `aspect-ratio` and fill it with a **deterministic** fallback (initials, a hashed color) so the same record always looks the same.
- **Distinguish absent from zero.** "0 members" is information; "—" is absence. Different meanings deserve different treatments.
- **Prefer omitting the row to rendering an empty label.** A label with nothing after it reads as a bug.

---

## `error-taxonomy`: Kind First, Then Placement · high

| Kind | Example | Treatment |
|---|---|---|
| **Transient** | network blip, timeout | inline retry at the failure site, input preserved |
| **User-fixable** | validation, card declined | at the field; say what to change, not that something is wrong |
| **Terminal** | 403, 404, 500, deleted record | explain plainly, offer the exit. **Never a dead end** |
| **Background** | autosave failed, sync dropped | persistent marker. **Not a toast.** Toasts expire, the problem does not |

**Placement.** The error appears **where the user's attention already is**. They
touched a control, so the response belongs at that control. A toast is for
something that happened outside their focus. **A validation error in a toast
makes the user hunt for their own mistake.**

**Three absolutes.** Never destroy user input on failure; a form that clears on
error is hostile. Retry is a control, not an instruction to reload. Cap repeated
retries and escalate to terminal, infinite spinner-retry loops are how users
learn to force-quit.

**Motion.** Error in at **120ms, opacity only, no slide**. Sliding or bouncing
reads as chatty about a moment the user is already unhappy in, and **shake is a
punishment animation**: almost never right. **Content must not move when an
error appears**: reserve the slot, or the submit button shifts down and the
user's next tap lands somewhere else.

**Retry is contained.** The pending state lives inside the button, the label
swaps to a spinner, the button keeps its width, the content region does **not**
collapse back to skeleton, scroll holds. That single rule is most of what makes
retry feel solid rather than like starting over.

**Error → success: dismiss, do not celebrate.** No success toast for a retry that
worked, the content arriving *is* the confirmation, and a toast reads as the app
congratulating itself for recovering from its own failure.

**Repeated failure escalates.** Second failure looks the same; third changes tone
and offers a different path. An error rendering identically five times reads as a
stuck UI.

---

## `optimistic-rollback`: The Reverse Is the Hard Part · high

> An invisible revert means the user believes their change stuck.

- **Optimistic → confirmed should be invisible.** If the confirmed render differs from the optimistic one (a real ID, a server timestamp, a formatted value) the settle flicker exposes the illusion. Make them identical, or accept a deliberate ~150ms transition and make the difference meaningful.
- **Rollback is slower than the apply.** Apply ~120ms, revert **~300ms** with a brief highlight. A revert as fast as the apply is imperceptible, and that is the line between optimistic UI and lying.
- **Mark, do not just revert.** The element returns to its old value **and** carries a failure marker until acknowledged. Silent rollback is the worst outcome in this whole category: the user is now working from a false model of their own data.
- **Never optimistic on destructive actions.** Deletion needs a real pending state, or an undo window with the row held dimmed. Removing a row and restoring it 800ms later is disorienting in a way no animation fixes.

---

## `overflow-pressure`: The Layout Under Load · high

> Cheap to test, and it is what breaks in production.

**The fixture set:**

- **Strings.** 1 char, 47 chars, no spaces, RTL, combining diacritics, emoji-only.
- **Numbers.** 0, negative, 1,000,000, a currency with no decimals, one with three.
- **Collections.** 0, 1, 2, 500.
- **Media.** 1:4 portrait, 4:1 panorama, 404, transparent PNG on a dark surface.

**Rules.** Truncate in **CSS, not JS.** JS truncation is wrong at every viewport
except the one you tested. Anything truncated stays reachable in full somewhere.
**Never truncate a number.** Wrap, abbreviate or shrink it, because a clipped
figure is misinformation rather than a display issue. Tabular numerals wherever
figures stack. A **two-line clamp beats a one-line ellipsis** on titles; most
names survive two lines.

---

## `offline-stale`: Is This Screen Lying? · medium

> For every value: if this is thirty minutes old, can the user act on it and be
> wrong?

- **If yes.** It needs a timestamp or a stale marker. Prices, availability, scores, balances, live status.
- **If no.** Cached silence is fine. Do not clutter static content with sync chrome.
- **Network-dependent actions are disabled or queued while offline.** Never failing silently on tap.
- **Queued actions need a visible queue.** "It'll sync later" is only true if the user can see that it hasn't yet.

---

## `permission-states`: 403 and 404 Are a Design Decision · medium

> Revealing that a record exists to someone not allowed to see it is a leak.

The two are different truths that often must look identical. **Decide
deliberately which you are doing and be consistent across the app,
inconsistency is itself the leak**, since the difference in response becomes the
signal.

**A permission-denied state names who *can* grant access.** "You don't have
access" with no path forward converts a permissions problem into a support
ticket.

---

## `end-of-list`: Terminus, Settled, and Continuity · medium

- **Paginated lists need a terminus.** "That's everything" is a small kindness; scrolling into silence reads as a failure to load.
- **Infinite scroll still needs an end state**, or a written decision that there isn't one.
- **Settled.** The moment *after* a successful action, is the state most often skipped because it seems obvious. What does the row look like one second after save? Where does focus go? Is the change visible without a refresh?

**Continuity across every transition:**

- **Focus survives the swap.** Focus inside a removed skeleton falls to `<body>`, keyboard users lose their place and screen reader users hear nothing. Re-anchor to the equivalent element or the container.
- **Announce state changes:** `aria-live="polite"` for empty and success, `assertive` for errors that block progress, `aria-busy` during load.
- **Scroll position holds** across retry, refetch, filter change and background update. Reset only when the user changed context.
- **New content above the viewport does not push.** Compensate scroll and offer a "3 new" affordance instead.

---

## AI-native surfaces need a longer list

Streaming, tool calls, retrieval and approval break the CRUD assumptions that a
request succeeds or fails, that success is complete on arrival, and that the same
request twice returns the same answer. Additional states: **streaming** (partial
output is never discarded), **working with no ETA** (elapsed time, never a
fabricated percentage; cancel from 500ms), **partial success** ("12 of 15" is a
third outcome, retry only the failures), **confidence**, **ungrounded**,
**refusal**, **awaiting approval** (blocked on the human, rendering it as a
spinner is why approvals sit for hours), and **regeneration ≠ retry**.

Full treatment in the `sad-paths` skill. This file does not duplicate it.
