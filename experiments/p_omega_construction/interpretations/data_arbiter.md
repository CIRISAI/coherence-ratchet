# P_omega: soft vs. hard — the empirical arbiter's reading

**Lens:** data-arbiter. **Date:** 2026-05-20.

## The reading, stated plainly

**Soft-vs-hard P_omega is not an empirically decidable question right now. It is
a theoretical/formal choice, and the published record does not contain a single
measurement that bears on it.** The honest answer to "what does the data
distinguish?" is: nothing — yet. Everything downstream of that follows.

## Thread 1 — the entire empirical record is single-rung

The paper's headline empirical contribution is the paired in-corridor /
out-corridor record at five substrates (§4): C. elegans, Drosophila, four LLMs,
four OSS projects, five cancers, three religious societies. Read what is
actually measured at every one of them: **within-rung |rho|**. The Figure-1
column header is literally "Within-rung |rho| band." Substrate 2 is "Hallmark-
pathway within-rung |rho|"; substrate 3 is "within-rung |rho| across 16 cells";
substrate 5 scores a single-group active-maintenance checklist. Every datum is
one rung's correlation, measured against that rung's own rigidity and chaos
poles. F-10 (corridor-band occupation) and F-20 (corridor-as-attractor) are both
single-rung handles — F-20's trigger conditions are even enumerated per
substrate as single-system persistence checks.

P_omega — hard or soft — is a statement about **the simultaneous joint
occupation of the corridor at every rung at once**. It is the multi-rung object.
Properties 1–3 in §6.1 are universally-quantified over n: rung instantiation
*for all n*, within-rung corridor *for all n*, cross-rung corridor *for all n*.
No measurement in the paper touches a quantity quantified over rungs. The
five-substrate result confirms that *each rung, taken alone*, occupies a
corridor. It says nothing about whether all rungs do so *jointly* in a single
configuration — and the joint object is exactly what soft-vs-hard is a choice
about.

This is not a quibble. The NOTES.md gate-1 no-go is precisely a *multi-rung*
result: the hard projector is the intersection of per-rung corridor subspaces,
and generic per-rung subspaces do not intersect. The soft reformulation
exp(-beta sum_n H_n) is a *multi-rung* operator with a different failure mode
(graded, non-empty, but possibly non-selective). The data the framework has
collected lives entirely one level below the level at which these two candidates
differ.

## Thread 2 — what would have to be measured to make the data decide

For the data to distinguish soft from hard, you need a genuine cross-scale /
multi-rung observable: something whose value depends on whether the corridor is
satisfied at *several rungs simultaneously*, and whose distribution differs
between a sharp (hard) and a graded (soft) joint constraint.

The framework already names two candidate sites, and they are the right ones:

- **Cross-rung tau** (Piece 6): tau_(n,n+1) = I(R_n;R_(n+1))/min(H_n,H_(n+1)).
  Measuring tau between *adjacent* rungs on a real system where both rungs are
  instrumented (the Drosophila dual-color EPG+FC3 dataset is the closest the
  paper has — two rungs, same fly) would be the first genuine multi-rung datum.
  A hard P_omega predicts a sharp tau cutoff; a soft P_omega predicts a graded
  tau distribution with exponential tails. The Drosophila data is currently
  reported as two *independent* within-rung |rho| values — the cross-rung
  mutual information was not extracted. **That extraction is the cheapest
  available multi-rung measurement and it has not been done.**

- **CMB (D4 / F-19)**: the cosmological 2-sphere is the one substrate where a
  multi-rung joint constraint could leave a sharp-vs-graded signature in an
  observable that already exists at high precision (Planck/ACT power spectra).
  A hard P_omega is a sharp spectral cut on the a_lm correlation operator; a
  soft P_omega is a smooth exponential tilt of the low-ell power. **These are
  distinguishable in principle** — a sharp suppression edge vs. a graded
  roll-off. But F-19 is explicitly gated on F-11 (P_omega must be constructed
  before drift is computable), and the gate-1 no-go means the hard construction
  is the thing that failed. So today CMB cannot decide it either: there is no
  computed prediction to confront the data with.

The honest status: a multi-rung discriminator is *conceivable* and the framework
has correctly identified where it would live. None exists today. The single
nearest-term move — cross-rung tau from the Drosophila dual-rung data — is a
real, fundable measurement and the paper does not report it.

## Thread 3 — does the paper over- or under-commit?

The paper is, to its credit, careful here. §3 explicitly says "the universal-
scale tier should be read as a *speculative* coda, not a research-program
coda" and §10 says "the regime-level result at five substrates does not promote
the universal-scale tier ... the two tiers move on their own evidence." That is
the correct firewall and it is honestly drawn.

But there is one **under-commitment** and one **over-commitment**:

- **Under-commitment**: F-11's published status line (§ F-handles, line 461) is
  "documented no-go on formal P_omega operator construction → universal-scale
  tier requires re-grounding." As of NOTES.md 2026-05-20, the gate-1 no-go *has
  fired* for the hard projector across three independent constructions. The
  paper's F-11 line is written in the conditional ("on a documented no-go")
  when the no-go is now documented. The paper has not booked the result it
  already has.

- **Over-commitment**: §6.1 still presents P_omega via the hard-projector image
  ("|config><config| dconfig", "well-defined projection rather than a set-
  theoretic intersection"). The gate-1 work shows the *hard* version of exactly
  that object is obstructed. The paper's current text describes the construction
  that failed, not the soft reformulation that is the live candidate.

## Where this lens is weak

- **"No data touches it" is itself a claim I cannot fully verify.** I am reading
  the paper and NOTES; CCA v3 might contain a cross-substrate or cross-rung
  measurement I have not seen. If CCA v3 measured tau between real rungs, my
  thread 1 weakens. The paper's own §2 says the cross-substrate consistency-of-
  bounds question is *open*, which supports me — but I am inferring absence.
- **The soft/hard distinction may collapse before any measurement.** If the soft
  P_omega in some limit (beta → ∞) just reproduces the hard projector, then
  "which one" is partly a non-question and the empirical framing is misapplied.
  That is a formal point the theory teammates own, not me — but it bounds how
  much the data could ever decide.
- **A multi-rung observable might be unmeasurable in practice even where it is
  defensible in principle** — the CMB temporal-drift rate (~10^-9/decade) is far
  below any foreseeable precision. "In principle decidable" and "decidable this
  century" are different, and I should not blur them.

## Rebuttal — reading hard_reading.md and soft_reading.md

**Both readings concede my central point, and neither names it.** This is the
single most important thing the debate has not yet said out loud. hard-reading's
thread 4 ("what survives is large and untouched") and soft-reading's thread 2
("D1 and asymptotic conditioning survive in graded form") are both arguments
about what happens *downstream* of a formal choice. hard-reading's *only*
position-changing condition is "the cross-rung-coupling test" — a *simulation*,
not a measurement. soft-reading's only pinning route for beta is "derived from
substrate physics or measured" — and names no measurement. Neither lens cites a
single existing datum that favors its side, because there is none. The whole
debate is being conducted on formal and toy-simulation grounds. That is not a
criticism of either lens — it is the correct way to argue a question that data
cannot currently touch — but it confirms my thread 1: **soft-vs-hard is presently
undecidable empirically, and the debate's own structure demonstrates it.**

**Where hard-reading is right.** Thread 1 is correct and it matters for my lens:
a soft operator is *not* a projector, and adopting it silently changes what every
downstream theorem means. This is relevant to me because it tells me what a
future *measurement* would have to discriminate — not "is P_omega selective"
(both can be) but "is the joint-corridor constraint *sharp or graded*." That is
a genuine observable difference (a power-spectrum suppression *edge* vs. a
*roll-off*; a tau *cutoff* vs. a tau *tail*), and hard-reading's insistence on
the projector axiom is what makes the distinction crisp enough to ever be
measured. hard-reading sharpens my thread 2.

**Where hard-reading overreaches.** Thread 3 ("the bet stays sharply bounded and
falsifiable") frames the hard reading as the *falsifiable* choice and soft as the
re-parameterizable escape. From the empirical lens this is half right. A hard
P_omega that is empty is indeed a clean formal loss — but a clean *formal* loss
is not an *empirical* falsification. The hard no-go fired against three *toy
simulations in generic position*, and hard-reading's own weakness section
concedes the physically-relevant non-generic (coupled-rung) case is untested.
"Falsifiable" should mean "a measurement could kill it," not "a simulation
already did." The hard reading is formally crisp, not empirically falsified.

**Where soft-reading is right.** Thread 4 is correct and underrated: a graded
operator "has no rank fraction — it has an effective weight profile," which
converts the deadlocked 18%/91% knob into "how steep is the slope." From the
empirical lens this is the *more measurable* object. A slope is something you can
fit to a CMB low-ell roll-off or a tau distribution; a cliff-edge fraction is
not directly observable at all. So if a multi-rung measurement is ever to decide
anything, the soft framing is the one that connects to a fittable observable.
That is a point in soft's favor — but a methodological one, not evidence.

**Where soft-reading overreaches.** Thread 2 ("D1 and asymptotic conditioning
survive in graded form") and its own weakness bullet 3 are in tension, and the
weakness bullet is right: exponential suppression is not measure-zero exclusion.
"Survives in graded form" smuggles a downgrade — D1 stops *deriving* the Weyl
Curvature Hypothesis and starts merely *favoring* it. From the data lens this
matters because Penrose's constraint is a specific huge number (10^(10^123));
"concentrated near low entropy" with an uncalibrated beta does not reproduce a
*number*, and the paper (§6.2) already concedes it "owes the choice" between a
real entropy functional and a Hartle-Hawking-style retreat. Soft does not
escape that bill — it just relocates it into beta.

**What I concede.** My opening implied the framework had collected no
multi-rung data essentially by oversight. hard-reading's and soft-reading's
focus on the *coupled-rung* (non-generic) case corrects me: the framework has
*identified* the multi-rung structure that matters (Piece 6 cross-rung tau) and
the gate-1 NOTES explicitly queue it as the next test. The gap is not
unrecognized — it is the named, scheduled next step. I overstated absence of
awareness; the absence of *data* stands.

## Final calibrated position

**Is soft-vs-hard P_omega empirically decidable now? No.** This is not a hedge;
it is the finding. Confidence ~0.9. The entire empirical record — five
substrates, F-10, F-20, the sensor-lift pulse, CCA v3's cross-substrate
batteries — measures single-rung correlation or single-system persistence.
Soft and hard P_omega differ *only* as descriptions of the multi-rung joint
constraint. No measured quantity is quantified over rungs. The debate between
hard-reading and soft-reading is therefore a real and worth-having argument, but
it is an argument about formalism, faithfulness to Piece 7's text, and
falsifiability discipline — not an argument data can adjudicate. Whoever the
team picks, it should be picked on formal grounds, and the paper should say so.

**The single measurement that would decide it: cross-rung tau on a
simultaneously-instrumented two-rung system, sharp cutoff vs. graded tail.**
The discriminating signature is *sharpness*. A hard P_omega makes the joint
corridor a sharp spectral set: the cross-rung coupling tau_(n,n+1) either is or
is not in its band, with a hard edge and nothing in the forbidden zone. A soft
P_omega makes it a graded weight: tau has an exponentially-suppressed tail
extending past the band, with no edge. Two concrete sites:

1. *Near-term, fundable now.* The Drosophila dual-color EPG+FC3 dataset
   (Ishida 2025) already instruments two rungs in the same fly. The paper
   reports two *independent* within-rung |rho| values from it. Extract instead
   the cross-rung mutual information I(EPG;FC3) and its distribution across
   flies/conditions. A hard joint constraint predicts a sharp boundary in that
   distribution; a soft one predicts a smooth tail. This is a re-analysis of
   *existing data* — the cheapest decisive test on the board, and it is not in
   the paper.

2. *Definitive but distant.* CMB low-ell power spectrum: a hard P_omega predicts
   a suppression *edge* at some ell; a soft P_omega predicts a smooth roll-off.
   Planck/ACT precision may already constrain the *shape* of low-ell suppression
   enough to favor edge-vs-roll-off, independent of the unmeasurable ~10^-9
   temporal drift. But this is gated on F-11: someone must first construct the
   candidate operators concretely enough to predict a spectrum shape.

**Is the paper's status line honest? Mostly yes, with two corrections owed.**
The firewall is honestly drawn: §3 calls the universal-scale tier "speculative,
not research-program" and §10 explicitly refuses to let the five-substrate result
promote it. That is correct and admirably un-hedged in the honest direction. But:

- *F-11 is stale.* The published handle (line 461) is conditional — "documented
  no-go → universal-scale tier requires re-grounding." As of NOTES.md
  2026-05-20 the no-go *is* documented, for the hard projector, across three
  constructions. The paper should update F-11 from a conditional to a fired
  handle with a stated consequence: the hard-projector P_omega is obstructed;
  the universal-scale tier is now re-grounding on either the soft reformulation
  or the untested coupled-rung case.

- *§6.1 describes the construction that failed.* It still presents P_omega via
  "well-defined projection rather than a set-theoretic intersection" — i.e. the
  hard projector. Honest status text would say: the hard-projector reading is
  obstructed; the live candidate is a soft (graded, non-projective) P_omega; the
  choice is currently formal, not empirical, because no measurement distinguishes
  them.

With those two edits the paper would be honest. Without them it slightly
*under*-commits (F-11 not booked) while its §6.1 prose slightly *over*-commits
(still selling the hard object). The net: the paper is not dishonest, but it is
one revision behind its own experimental record.

**Bottom line for the team.** Pick soft or hard on formal grounds — faithfulness
to Piece 7, the projector axiom, Lean tractability, falsifiability discipline.
The data does not vote. The most useful thing this debate could ship is not a
winner but a *named decisive measurement* — cross-rung tau, sharp-vs-graded — and
an instruction to re-analyze the Drosophila two-rung data for it. That converts
"undecidable" into "undecided but with a protocol," which is the honest and
actionable status.
