/**
 * recall — how much of its own past a persona is allowed to bring.
 *
 * Two properties decide what a persona is, and they are orthogonal:
 *
 *   lifespan  does this persona outlive the run?
 *             persistent — lives in the library, reusable, accumulates history
 *             temporary  — exists for this run only, stored in the run folder
 *
 *   recall    how much of its own history may it read when dispatched?
 *             none     never. A first impression is a non-renewable resource.
 *             artifact only prior encounters with THIS artifact — the same
 *                      problem, still ongoing.
 *             project  encounters across artifacts in the same project or
 *                      category.
 *             all      everything it has ever seen.
 *
 * The point of the split: some personas' value is CUMULATIVE and some is
 * NON-RENEWABLE. An architect who forgets prior assessments is a worse
 * architect — memory is the whole reason to keep it. A first-run user who
 * remembers is no longer a first-run user — memory destroys the instrument, and
 * unlike the architect's, that loss cannot be undone. You can always give a
 * persona context; you can never give it back its first look.
 *
 * So `none` is the default. The failure mode of wrongly-fresh is recoverable
 * (dispatch again with context). The failure mode of wrongly-cumulative is not.
 *
 * WRITING is never gated. Every persona records what it saw, because the
 * analyst needs it even when the persona may not read it. Only READING is
 * scoped.
 */

import { listEncounters } from "./encounters.mjs";

export const RECALL_SCOPES = ["none", "artifact", "project", "all"];
export const LIFESPANS = ["persistent", "temporary"];

export function isRecallScope(v) {
  return typeof v === "string" && RECALL_SCOPES.includes(v);
}

export function personaRecall(persona) {
  return isRecallScope(persona?.recall) ? persona.recall : "none";
}

export function personaLifespan(persona) {
  return LIFESPANS.includes(persona?.lifespan) ? persona.lifespan : "persistent";
}

/**
 * The encounters a persona is PERMITTED to be shown for a given context.
 * Returns [] for scope "none" — not an error, just an empty briefing.
 */
export function permittedEncounters(persona, { artifact, project } = {}) {
  const scope = personaRecall(persona);
  if (scope === "none") return [];

  const mine = listEncounters({ persona_id: persona.id });
  if (scope === "all") return mine;

  if (scope === "artifact") {
    if (!artifact) return [];
    return mine.filter((e) => e.artifact?.slug === artifact);
  }

  // project: same project/category, whatever artifact within it
  if (!project) return [];
  return mine.filter((e) => e.artifact?.project === project);
}

/**
 * Judge a proposed informed dispatch. Returns { ok, errors, permitted }.
 * `shown` is the list of encounter_ids the dispatcher wants to hand over.
 */
export function checkRecallRequest(persona, shown = [], context = {}) {
  const scope = personaRecall(persona);
  const errors = [];

  if (scope === "none" && shown.length) {
    errors.push(
      `persona ${persona.id} has recall "none" and cannot be shown prior encounters. ` +
      "Its value is the unanchored first look, which only happens once. " +
      "If you want a version that carries history, that is a different persona."
    );
    return { ok: false, errors, permitted: [] };
  }

  const permitted = permittedEncounters(persona, context);
  const allowed = new Set(permitted.map((e) => e.encounter_id));
  const own = new Set(listEncounters({ persona_id: persona.id }).map((e) => e.encounter_id));
  for (const id of shown) {
    if (allowed.has(id)) continue;
    // Two different refusals. Recall governs a persona's OWN history; handing it
    // someone else's transcript is not a narrow scope, it is a different act —
    // that is a debate round, and it belongs in a debate lane.
    if (!own.has(id)) {
      errors.push(
        `encounter ${id} does not belong to ${persona.id}. Recall carries a persona's ` +
        "own history. Showing it another persona's position is a debate round — run " +
        "it as a debate lane after the blind passes are saved."
      );
    } else {
      errors.push(
        `encounter ${id} is the persona's own but falls outside recall scope "${scope}"` +
        (context.artifact ? ` for artifact "${context.artifact}"` : "") +
        (context.project ? ` / project "${context.project}"` : "") +
        ". Widen the persona's recall, or pass the matching context."
      );
    }
  }
  return { ok: errors.length === 0, errors, permitted };
}

/**
 * A briefing packet for a cumulative persona: what it already knows, ordered
 * so the same-problem history leads. Verbatim is never trimmed — a summarised
 * memory is a memory the persona will rationalise from rather than recall.
 */
export function buildRecallBriefing(persona, { artifact, project, limit = 6 } = {}) {
  const scope = personaRecall(persona);
  const permitted = permittedEncounters(persona, { artifact, project });

  // Same artifact first — that is the ongoing problem — then the rest, newest first.
  const sameArtifact = permitted.filter((e) => artifact && e.artifact?.slug === artifact);
  const others = permitted.filter((e) => !(artifact && e.artifact?.slug === artifact));
  const ordered = [...sameArtifact, ...others].slice(0, limit);

  return {
    persona_id: persona.id,
    persona_name: persona.name,
    recall: scope,
    context: { artifact: artifact || null, project: project || null },
    available: permitted.length,
    included: ordered.length,
    encounter_ids: ordered.map((e) => e.encounter_id),
    briefing: ordered.map((e) => ({
      encounter_id: e.encounter_id,
      run_id: e.run_id || null,
      artifact: e.artifact,
      when: e.started_at,
      blind: e.blind,
      verbatim: e.verbatim,
      standing_findings: (e.findings || [])
        .filter((f) => f.verified === "confirmed" || f.verified === "reclassified")
        .map((f) => ({ kind: f.kind, claim: f.claim, verified: f.verified, note: f.verification_note })),
      unanswered: e.unanswered || [],
    })),
  };
}

export function renderRecallBriefing(pack) {
  const L = [];
  L.push(`# What ${pack.persona_name || pack.persona_id} already knows`);
  L.push("");
  L.push(`Recall scope: **${pack.recall}**${pack.context.artifact ? ` · artifact \`${pack.context.artifact}\`` : ""}${pack.context.project ? ` · project \`${pack.context.project}\`` : ""}`);
  L.push(`Showing ${pack.included} of ${pack.available} permitted encounters.`);
  L.push("");
  if (pack.recall === "none") {
    L.push("This persona carries no history by design. Its value is the unanchored");
    L.push("first look, and that only happens once. Dispatch it blind.");
    L.push("");
    return L.join("\n");
  }
  if (!pack.included) {
    L.push("_Nothing on record yet in this scope. This dispatch is effectively a first look._");
    L.push("");
    return L.join("\n");
  }
  for (const b of pack.briefing) {
    L.push(`## ${b.artifact?.label || b.artifact?.slug}${b.artifact?.version ? ` @ ${b.artifact.version}` : ""} — ${String(b.when).slice(0, 10)}`);
    L.push("");
    L.push(`\`${b.encounter_id}\`${b.run_id ? ` · run \`${b.run_id}\`` : ""} · ${b.blind ? "was a blind read" : "was an informed read"}`);
    L.push("");
    L.push("What you said then, unedited:");
    L.push("");
    L.push("> " + String(b.verbatim).split("\n").join("\n> "));
    L.push("");
    if (b.standing_findings.length) {
      L.push("Findings that survived verification:");
      for (const f of b.standing_findings) {
        L.push(`- ${f.claim} (${f.kind}, ${f.verified}${f.note ? ` — ${f.note}` : ""})`);
      }
      L.push("");
    }
    if (b.unanswered.length) {
      L.push("You could not settle these:");
      for (const q of b.unanswered) L.push(`- ${q}`);
      L.push("");
    }
  }
  L.push("---");
  L.push("");
  L.push("This is your own history. React to the artifact in front of you now; do not");
  L.push("defend a position because it was yours. A changed mind is a finding.");
  L.push("");
  return L.join("\n");
}
