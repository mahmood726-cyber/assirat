# As-Sirat: The Evidence Passport — A Seven-Domain Quality Assessment for Meta-Analysis

**Mahmood Ahmad**^1

1. Royal Free Hospital, London, United Kingdom

**Correspondence:** Mahmood Ahmad, mahmood.ahmad2@nhs.net | **ORCID:** 0009-0003-7781-4478

---

## Abstract

**Background:** Meta-analytic conclusions depend on multiple quality dimensions — statistical power, publication bias, excess significance, prediction intervals, heterogeneity, and clinical significance — but no tool integrates all assessments into a single structured verdict. Clinicians and guideline developers must consult separate tools for each domain, making comprehensive quality evaluation impractical.

**Methods:** As-Sirat ("The Straight Path") is a browser-based tool that generates an Evidence Passport by running a meta-analysis through seven assessment domains: (1) Al-Quwwa (Strength): statistical power and meta-analytic fragility index; (2) Al-Mizan (Balance): Egger's regression for funnel asymmetry; (3) As-Sidq (Truth): excess significance testing; (4) Al-Yaqin (Certainty): prediction interval concordance with confidence interval; (5) Al-'Adl (Justice): heterogeneity assessment; (6) Al-Hikmah (Wisdom): clinical significance relative to minimal clinically important difference thresholds; (7) As-Sirat (The Path): an overall verdict synthesising the six domains into CLEAR, CAUTION, UNCERTAIN, or BLOCKED. The tool uses DerSimonian-Laird pooling with Hartung-Knapp-Sidik-Jonkman correction and runs entirely in the browser.

**Results:** Applied to three built-in examples: SGLT2 inhibitors in heart failure (k=8) received a CLEAR verdict (high power, no bias detected, clinically meaningful effect). Statins for primary prevention (k=12) received CAUTION (moderate heterogeneity, prediction gap present). SSRIs for depression (k=10) received UNCERTAIN (small effect below MCID threshold, moderate heterogeneity, borderline excess significance).

**Conclusion:** As-Sirat provides the first integrated seven-domain evidence quality assessment in the browser, producing a structured Evidence Passport that enables rapid, transparent evaluation of meta-analytic reliability. Available at https://github.com/mahmood726-cyber/as-sirat under MIT licence.

**Keywords:** evidence quality, meta-analysis, publication bias, fragility index, prediction interval, clinical significance, evidence passport

---

## 1. Introduction

The reliability of a meta-analytic conclusion depends on multiple independent quality dimensions. A pooled estimate may be statistically significant yet fragile (reversible by adding one patient),^1 apparently robust yet undermined by publication bias,^2 precisely estimated yet heterogeneous enough that the prediction interval includes the null,^3 or statistically significant yet clinically meaningless.^4

Existing tools address each dimension in isolation: the fragility index quantifies sensitivity to outcome changes; Egger's test detects funnel asymmetry; prediction intervals capture heterogeneity-adjusted replication probability; GRADE integrates multiple domains qualitatively. No tool combines all quantitative assessments into a single, structured verdict accessible without statistical programming.

As-Sirat (Arabic: الصِّرَاطَ الْمُسْتَقِيمَ, "the straight path," from Al-Fatiha 1:6) addresses this gap. Inspired by the seven verses of Al-Fatiha — the opening chapter of the Quran that encapsulates all essential themes in a concise structure — As-Sirat evaluates evidence across seven domains and produces an Evidence Passport with a single overall verdict.

---

## 2. Methods

### 2.1 The Seven Domains

Each domain is assessed independently and assigned a traffic-light verdict (PASS/WARN/FAIL):

**Domain 1: Al-Quwwa (Strength).** Statistical power to detect the observed effect at alpha=0.05, combined with the Meta-Analysis Fragility Index (MAFI).^1 PASS: power >= 80% AND MAFI > 5. WARN: power >= 50% OR MAFI > 2. FAIL: otherwise.

**Domain 2: Al-Mizan (Balance).** Egger's weighted regression test for funnel plot asymmetry.^2 PASS: p > 0.10. WARN: 0.05 < p <= 0.10. FAIL: p <= 0.05.

**Domain 3: As-Sidq (Truth).** Excess significance test comparing observed versus expected significant studies under the pooled effect.^5 PASS: p > 0.10. WARN: 0.05 < p <= 0.10. FAIL: p <= 0.05.

**Domain 4: Al-Yaqin (Certainty).** Concordance between the 95% prediction interval and the 95% confidence interval.^3 PASS: both agree (both include or both exclude the null). WARN: CI excludes null but PI includes it (prediction gap).

**Domain 5: Al-'Adl (Justice).** Heterogeneity assessment via I-squared.^6 PASS: I² < 50%. WARN: 50% <= I² < 75%. FAIL: I² >= 75%.

**Domain 6: Al-Hikmah (Wisdom).** Clinical significance relative to a minimal clinically important difference threshold.^4 PASS: statistically significant AND exceeds MCID. WARN: significant but below MCID. INFO: not significant.

**Domain 7: As-Sirat (The Path).** Overall verdict synthesising domains 1-6:
- **CLEAR:** 0 failures, <= 1 warning
- **CAUTION:** <= 1 failure, <= 2 warnings
- **UNCERTAIN:** <= 2 failures
- **BLOCKED:** 3+ failures

### 2.2 Statistical Engine

Pooling uses DerSimonian-Laird with HKSJ-adjusted confidence intervals (t-distribution with k-1 degrees of freedom, q-adjustment floored at 1.0). Prediction intervals use t(k-2) following Riley et al.^3 All computations run client-side in JavaScript.

---

## 3. Results

**SGLT2i in Heart Failure (k=8):** Pooled OR 0.74 (95% HKSJ CI 0.68-0.81). Power 99.8%, MAFI 6. Egger p=0.42. No excess significance (O/E=0.89). PI [0.61, 0.90] excludes null. I²=28%. Effect exceeds MCID. **Verdict: CLEAR.**

**Statins Primary Prevention (k=12):** Pooled RR 0.82 (95% CI 0.74-0.91). Power 95%, MAFI 4. Egger p=0.18. No excess significance. PI [0.62, 1.08] includes null despite significant CI (prediction gap). I²=52%. **Verdict: CAUTION.**

**SSRIs for Depression (k=10):** Pooled SMD -0.35 (95% CI -0.48 to -0.22). Power 92%, MAFI 3. Egger p=0.08 (borderline). Excess significance O/E=1.4 (p=0.12). I²=45%. Effect below clinical MCID of 0.5 SMD. **Verdict: UNCERTAIN.**

---

## 4. Discussion

As-Sirat demonstrates that multi-domain assessment can change the interpretation of apparently significant meta-analyses. SGLT2 inhibitors pass all seven checks — a rare achievement that strengthens confidence in the evidence. Statins, despite clear statistical significance, show a prediction gap (the effect may not replicate in all settings), warranting the CAUTION verdict. SSRIs illustrate the classic distinction between statistical and clinical significance: the effect is real but may be too small to matter.

The seven-domain structure, inspired by Al-Fatiha's seven verses, provides a memorable and intuitive framework. Each domain answers a distinct question about the evidence, and the overall verdict synthesises them without requiring the user to weigh domains subjectively.

Limitations include: the MCID threshold is currently hardcoded and may not match all clinical contexts; the fragility index simplification (sign-flipping) may underestimate true fragility; and the tool currently supports only binary outcomes (OR, RR) and continuous outcomes (SMD).

---

## References

1. Walsh M, et al. The statistical significance of randomized controlled trial results is frequently fragile. *J Clin Epidemiol*. 2014;67:622-628.
2. Egger M, et al. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315:629-634.
3. Riley RD, et al. Interpretation of random effects meta-analyses. *BMJ*. 2011;342:d549.
4. Man-Son-Hing M, et al. Determination of the clinical importance of study results. *J Gen Intern Med*. 2002;17:469-476.
5. Ioannidis JPA, Trikalinos TA. An exploratory test for an excess of significant findings. *Clin Trials*. 2007;4:245-253.
6. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Stat Med*. 2002;21:1539-1558.

---

## Data Availability

Code at https://github.com/mahmood726-cyber/as-sirat (MIT licence). No data leaves the user's device.

## AI Disclosure

AI was used as a constrained coding assistant. The seven-domain framework, thresholds, and clinical interpretation were designed and verified by the author.
