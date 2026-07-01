import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def logged_in_page(page):
    page.goto("https://admin.odakyu.bravesoft.vn/login")
    page.locator("[name='email']").fill("kimtran@bravesoft.com.vn")
    page.locator("#password").fill("brave0404")
    page.get_by_role("button", name="ログイン").click()
    expect(page).to_have_url("https://admin.odakyu.bravesoft.vn/account-management")
    return page

def test_login(logged_in_page):
    pass    

def test_画面タイトル(logged_in_page): 
    logged_in_page.get_by_role("button", name="新規追加").click()
    expect(logged_in_page.locator(".title-confirm")).to_be_visible()
    
def test_URL(logged_in_page):
    expect(logged_in_page).to_have_url("https://admin.odakyu.bravesoft.vn/account-management")
    
def test_check_label_アカウント名(logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    label = logged_in_page.locator(".label-title", has_text="アカウント名")
    expect(label).to_be_visible()
    expect(label.locator(".required-mark",has_text="*")).to_be_visible()
    expect(label.locator(".input-note",has_text="（255文字以内）")).to_be_visible()
    
def test_check_field_アカウント名(logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    logged_in_page.locator("[name='userName']").fill("Quynh Nguyen")
    expect(logged_in_page.locator("[name='userName']")).to_have_value("Quynh Nguyen")

def test_check_label_メールアドレス(logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    label = logged_in_page.locator(".label-title", has_text="メールアドレス")
    expect(label).to_be_visible()
    expect(label.locator(".required-mark",has_text="*")).to_be_visible()
    
def test_check_field_メールアドレス(logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    logged_in_page.locator("[name='email']").fill("quynhnguyen@bravesoft.com.vn")
    expect(logged_in_page.locator("[name='email']")).to_have_value("quynhnguyen@bravesoft.com.vn")
    
def test_check_label_パスワード(logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    label = logged_in_page.locator(".label-title", has_text="パスワード")
    expect(label).to_be_visible()
    expect(label.locator(".required-mark",has_text="*")).to_be_visible()
    expect(label.locator(".input-note",has_text="（半角英数字 8文字以上32文字以内）")).to_be_visible()
    
def test_check_field_パスワード(logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    expect(logged_in_page.get_by_placeholder("**********")).to_be_visible()
    logged_in_page.get_by_placeholder("**********").fill("brave0404")
    expect(logged_in_page.get_by_placeholder("**********")).to_have_value("brave0404")
    
def test_check_権限_case10 (logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    authority_section = logged_in_page.locator(".label-input", has_text="権限")
    expect(authority_section.locator(".multiselect-wrapper")).to_be_visible()
    expect(authority_section.locator(".multiselect-caret")).to_be_visible()
    expect(authority_section.locator(".multiselect-dropdown.is-hidden")).to_be_attached()
    
def test_check_権限_case11 (logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    authority_section = logged_in_page.locator(".label-input", has_text="権限")
    authority_section.locator(".multiselect-wrapper").click()
    authority_section.get_by_text("マスター管理者").click()
    expect(authority_section.locator(".multiselect-single-label")).to_have_text("マスター管理者")

def test_check_権限_case12 (logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    authority_section = logged_in_page.locator(".label-input", has_text="権限")
    authority_section.locator(".multiselect-wrapper").click()
    authority_section.get_by_text("テナント管理者").click()
    authority_section.locator(".multiselect-wrapper").click()
    authority_section.get_by_text("マスター管理者").click()
    expect(authority_section.locator(".multiselect-wrapper")).to_have_attribute("aria-multiselectable", "false")
    
def test_check_case13 (logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    authority_section = logged_in_page.locator(".label-input", has_text="権限")
    authority_section.locator(".multiselect-wrapper").click()
    authority_section.get_by_text("テナント管理者").click()
    
    content = logged_in_page.locator(".label-input", has_text="コンテンツ")
    content.locator(".multiselect-wrapper").click()
    content.get_by_text("チケット非表示").click()
    
    points_awarded = logged_in_page.locator(".label-input", has_text=" ポイント付与の有無（コンテンツに紐づく設定項目）")
    expect(points_awarded.locator("#pointAward1")).to_be_visible()
    expect(points_awarded.locator("label[for='pointAward1']")).to_have_text("有")
    expect(points_awarded.locator("#pointAward2")).to_be_visible()
    expect(points_awarded.locator("label[for='pointAward2']")).to_have_text("無")

def test_check_case1415 (logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    authority_section = logged_in_page.locator(".label-input", has_text="権限")
    authority_section.locator(".multiselect-wrapper").click()
    authority_section.get_by_text("テナント管理者").click()
    
    content = logged_in_page.locator(".label-input", has_text="コンテンツ")
    content.locator(".multiselect-wrapper").click()
    content.get_by_text("チケット非表示").click()
    
    points_awarded = logged_in_page.locator(".label-input", has_text=" ポイント付与の有無（コンテンツに紐づく設定項目）")
    points_awarded.locator("label[for='pointAward1']").click()
    expect(points_awarded.locator("#pointAward1")).to_be_checked()
    
    points_awarded = logged_in_page.locator(".label-input", has_text=" ポイント付与の有無（コンテンツに紐づく設定項目）")
    points_awarded.locator("label[for='pointAward2']").click()
    expect(points_awarded.locator("#pointAward2")).to_be_checked()

def test_check_case16 (logged_in_page):
    logged_in_page.get_by_role("button", name="新規追加").click()
    authority_section = logged_in_page.locator(".label-input", has_text="権限")
    authority_section.locator(".multiselect-wrapper").click()
    authority_section.get_by_text("テナント管理者").click()
    
    content = logged_in_page.locator(".label-input", has_text="コンテンツ")
    content.locator(".multiselect-wrapper").click()
    content.get_by_text("チケット非表示").click()
    
    points_awarded = logged_in_page.locator(".label-input", has_text=" ポイント付与の有無（コンテンツに紐づく設定項目）")
    points_awarded.locator("label[for='pointAward1']").click()
    points_awarded.locator("label[for='pointAward2']").click()
    expect(points_awarded.locator("#pointAward1")).not_to_be_checked()