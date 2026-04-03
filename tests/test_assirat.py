"""
Selenium test suite for As-Sirat: The Evidence Passport (7-domain meta-analysis tool).
~20 tests covering page load, examples, domains, verdicts, UI controls, and export.
"""
import os
import sys
import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "as-sirat.html")
FILE_URL = "file:///" + os.path.abspath(HTML_PATH).replace("\\", "/")

VALID_VERDICTS = {"CLEAR", "CAUTION", "UNCERTAIN", "BLOCKED"}
DOMAIN_VERDICTS = {"pass", "warn", "fail", "info"}


@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,1024")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(3)
    # Override confirm/alert to avoid blocking
    drv.get(FILE_URL)
    drv.execute_script("window.alert = function(){}; window.confirm = function(){return true};")
    yield drv
    drv.quit()


def _load_example(driver, idx):
    """Load example by index via JS and wait for passport to appear."""
    driver.execute_script("window.alert = function(){}; window.confirm = function(){return true};")
    driver.execute_script(f"loadExample({idx})")
    WebDriverWait(driver, 5).until(
        lambda d: "visible" in d.find_element(By.ID, "passport").get_attribute("class")
    )


# ========== 1. Page Load ==========

def test_01_page_loads_title(driver):
    """Page loads and title contains 'As-Sirat'."""
    assert "As-Sirat" in driver.title


def test_02_arabic_text_visible(driver):
    """Arabic calligraphic text is visible in header."""
    arabic_el = driver.find_element(By.CSS_SELECTOR, ".arabic")
    assert arabic_el.is_displayed()
    text = arabic_el.text
    assert "الصِّرَاطَ" in text


def test_03_data_card_visible(driver):
    """Data entry card is visible on load."""
    card = driver.find_element(By.ID, "data-card")
    assert card.is_displayed()


# ========== 2. Example Loading ==========

def test_04_load_example_sglt2i(driver):
    """Example 0 (SGLT2i HF k=8) loads and passport becomes visible."""
    _load_example(driver, 0)
    passport = driver.find_element(By.ID, "passport")
    assert "visible" in passport.get_attribute("class")


def test_05_load_example_statins(driver):
    """Example 1 (Statins Prevention k=12) loads correctly."""
    _load_example(driver, 1)
    rows = driver.find_elements(By.CSS_SELECTOR, "#study-rows .data-grid")
    assert len(rows) == 12


def test_06_load_example_ssris(driver):
    """Example 2 (SSRIs Depression k=10) loads correctly."""
    _load_example(driver, 2)
    rows = driver.find_elements(By.CSS_SELECTOR, "#study-rows .data-grid")
    assert len(rows) == 10


# ========== 3. Overall Verdict ==========

def test_07_overall_grade_valid_verdict(driver):
    """Overall grade shows a valid verdict string."""
    _load_example(driver, 0)
    grade_el = driver.find_element(By.ID, "overallGrade")
    assert grade_el.text.strip() in VALID_VERDICTS


def test_08_overall_grade_has_css_class(driver):
    """Overall grade element has the appropriate grade-* CSS class."""
    grade_el = driver.find_element(By.ID, "overallGrade")
    cls = grade_el.get_attribute("class")
    verdict = grade_el.text.strip()
    assert f"grade-{verdict}" in cls


def test_09_overall_label_not_empty(driver):
    """Overall label is generated and non-empty."""
    label = driver.find_element(By.ID, "overallLabel")
    assert len(label.text.strip()) > 10


# ========== 4. Seven Domains ==========

def test_10_all_seven_domains_rendered(driver):
    """All 7 domains are rendered in the passport."""
    _load_example(driver, 0)
    domains = driver.find_elements(By.CSS_SELECTOR, "#domains .domain")
    assert len(domains) == 7


def test_11_each_domain_has_verdict_class(driver):
    """Each domain element has a verdict class (pass/warn/fail/info)."""
    domains = driver.find_elements(By.CSS_SELECTOR, "#domains .domain")
    for d in domains:
        cls = d.get_attribute("class")
        has_verdict = any(v in cls.split() for v in DOMAIN_VERDICTS)
        assert has_verdict, f"Domain missing verdict class: {cls}"


def test_12_each_domain_has_verdict_text(driver):
    """Each domain has a non-empty verdict text element."""
    verdicts = driver.find_elements(By.CSS_SELECTOR, "#domains .domain-verdict")
    assert len(verdicts) == 7
    for v in verdicts:
        assert len(v.text.strip()) > 0


def test_13_domain_names_present(driver):
    """Expected domain names appear in the passport."""
    expected_names = ["Al-Quwwa", "Al-Mizan", "As-Sidq", "Al-Yaqin", "Al-'Adl", "Al-Hikmah", "As-Sirat"]
    name_els = driver.find_elements(By.CSS_SELECTOR, "#domains .domain-name")
    found_names = [el.text for el in name_els]
    for name in expected_names:
        assert any(name in fn for fn in found_names), f"Domain '{name}' not found in: {found_names}"


# ========== 5. Summary Table ==========

def test_14_summary_table_has_pooled_estimate(driver):
    """Summary table contains pooled estimate row."""
    _load_example(driver, 0)
    table_text = driver.find_element(By.ID, "summaryTable").text
    assert "Pooled" in table_text
    assert "Studies" in table_text


def test_15_summary_table_has_i_squared(driver):
    """Summary table shows I-squared value."""
    table_text = driver.find_element(By.ID, "summaryTable").text
    assert "%" in table_text  # I2 displayed with %


def test_16_summary_table_shows_overall(driver):
    """Summary table includes the overall path verdict."""
    table_text = driver.find_element(By.ID, "summaryTable").text
    has_verdict = any(v in table_text for v in VALID_VERDICTS)
    assert has_verdict, f"No verdict in summary table: {table_text}"


# ========== 6. Report Text ==========

def test_17_report_text_generated(driver):
    """Report text is generated and contains key sections."""
    _load_example(driver, 1)
    report = driver.find_element(By.ID, "reportText").text
    assert len(report) > 100
    assert "EVIDENCE PASSPORT" in report
    assert "SEVEN-DOMAIN ASSESSMENT" in report
    assert "OVERALL VERDICT" in report


# ========== 7. Theme Toggle ==========

def test_18_theme_toggle_changes_attribute(driver):
    """Theme toggle switches data-theme between dark and light."""
    html_el = driver.find_element(By.TAG_NAME, "html")
    initial_theme = html_el.get_attribute("data-theme")
    driver.execute_script("toggleTheme()")
    new_theme = html_el.get_attribute("data-theme")
    assert new_theme != initial_theme
    assert new_theme in ("dark", "light")
    # Toggle back
    driver.execute_script("toggleTheme()")
    restored = html_el.get_attribute("data-theme")
    assert restored == initial_theme


# ========== 8. UI Controls ==========

def test_19_add_row_button_adds_study(driver):
    """Add Row button increases the study count."""
    _load_example(driver, 0)
    rows_before = len(driver.find_elements(By.CSS_SELECTOR, "#study-rows .data-grid"))
    driver.execute_script("addRow()")
    rows_after = len(driver.find_elements(By.CSS_SELECTOR, "#study-rows .data-grid"))
    assert rows_after == rows_before + 1


def test_20_clear_button_hides_passport(driver):
    """Clear button removes passport visibility and clears studies."""
    _load_example(driver, 0)
    passport = driver.find_element(By.ID, "passport")
    assert "visible" in passport.get_attribute("class")
    driver.execute_script("clearAll()")
    assert "visible" not in passport.get_attribute("class")
    rows = driver.find_elements(By.CSS_SELECTOR, "#study-rows .data-grid")
    assert len(rows) == 0


def test_21_export_json_button_exists(driver):
    """Export JSON button exists in the report section."""
    _load_example(driver, 0)
    buttons = driver.find_elements(By.CSS_SELECTOR, ".btn-outline")
    btn_texts = [b.text for b in buttons]
    assert any("Export JSON" in t for t in btn_texts), f"Export JSON not found among: {btn_texts}"


def test_22_examples_produce_different_verdicts_or_k(driver):
    """Different examples produce different study counts (k=8, k=12, k=10)."""
    expected_k = {0: 8, 1: 12, 2: 10}
    for idx, k in expected_k.items():
        _load_example(driver, idx)
        rows = driver.find_elements(By.CSS_SELECTOR, "#study-rows .data-grid")
        assert len(rows) == k, f"Example {idx}: expected k={k}, got {len(rows)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
