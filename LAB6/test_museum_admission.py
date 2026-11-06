import pytest
from museum_admission import ticket_price, group_discount, gallery_entry

# --- Starter test cases from lab ---
def test_adult_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300

def test_small_group():
    assert group_discount(4, False) == 0

# --- Code Coverage Tests (targeting statement execution across all functions) ---
def test_ticket_price_invalid_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("invalid_cat", 25, "monday", False)

def test_ticket_price_invalid_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -5, "monday", False)

def test_ticket_price_under_five_free():
    assert ticket_price("child", 4, "monday", False) == 0

def test_ticket_price_monday_discount():
    assert ticket_price("adult", 30, "monday", False) == 150

def test_ticket_price_weekend_surcharge():
    assert ticket_price("senior", 65, "saturday", False) == 250

def test_ticket_price_student_guided_tour():
    assert ticket_price("student", 20, "wednesday", True) == 200

def test_ticket_price_adult_guided_tour():
    assert ticket_price("adult", 40, "friday", True) == 400

def test_group_discount_invalid_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)

def test_group_discount_school_large():
    assert group_discount(25, True) == 40

def test_group_discount_school_standard():
    assert group_discount(12, True) == 25

def test_group_discount_regular_large():
    assert group_discount(18, False) == 20

def test_group_discount_regular_medium():
    assert group_discount(10, False) == 10

def test_gallery_entry_wait():
    assert gallery_entry(100, 100, False) == "wait"

def test_gallery_entry_queue():
    assert gallery_entry(95, 100, False) == "queue"

def test_gallery_entry_enter():
    assert gallery_entry(50, 100, False) == "enter"
