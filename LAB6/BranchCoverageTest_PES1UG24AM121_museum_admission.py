import pytest
from museum_admission import ticket_price, group_discount, gallery_entry

# ============================================================================
# Branch Coverage Test Suite for museum_admission.py
# Designed to cover every decision branch and boolean sub-condition (100% branch coverage)
# ============================================================================

# --- ticket_price() Branch Coverage Tests ---

def test_ticket_price_category_invalid():
    # Branch: category not in BASE_PRICE -> True
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 25, "monday", False)

def test_ticket_price_age_negative():
    # Branch: age < 0 -> True
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "monday", False)

def test_ticket_price_under_five_boundary_zero():
    # Branch: age < 5 -> True (lower boundary: age = 0)
    assert ticket_price("child", 0, "monday", False) == 0

def test_ticket_price_under_five_boundary_four():
    # Branch: age < 5 -> True (upper boundary: age = 4)
    assert ticket_price("child", 4, "sunday", True) == 0

def test_ticket_price_age_five_regular():
    # Branch: age < 5 -> False (boundary: age = 5)
    assert ticket_price("child", 5, "wednesday", False) == 100

def test_ticket_price_monday_discount():
    # Branch: day == "monday" -> True (half price)
    # 300 // 2 = 150
    assert ticket_price("adult", 30, "monday", False) == 150

def test_ticket_price_saturday_surcharge():
    # Branch: day in ("saturday", "sunday") -> True via "saturday"
    # 200 + 50 = 250
    assert ticket_price("senior", 65, "saturday", False) == 250

def test_ticket_price_sunday_surcharge():
    # Branch: day in ("saturday", "sunday") -> True via "sunday"
    # 300 + 50 = 350
    assert ticket_price("adult", 25, "sunday", False) == 350

def test_ticket_price_regular_day_no_surcharge():
    # Branch: day not monday and not weekend -> False
    assert ticket_price("adult", 30, "tuesday", False) == 300

def test_ticket_price_student_with_guided_tour():
    # Branch: with_guided_tour -> True, category == "student" -> True
    # 150 + 50 = 200
    assert ticket_price("student", 20, "thursday", True) == 200

def test_ticket_price_non_student_with_guided_tour():
    # Branch: with_guided_tour -> True, category == "student" -> False
    # 300 + 100 = 400
    assert ticket_price("adult", 45, "thursday", True) == 400

def test_ticket_price_senior_weekday():
    # Cover senior base category with no tour
    assert ticket_price("senior", 70, "friday", False) == 200


# --- group_discount() Branch Coverage Tests ---

def test_group_discount_invalid_size_zero():
    # Branch: group_size < 1 -> True (boundary: 0)
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, True)

def test_group_discount_invalid_size_negative():
    # Branch: group_size < 1 -> True (negative size)
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(-5, False)

def test_group_discount_school_large_boundary():
    # Branch: is_school -> True, group_size >= 20 -> True (boundary: 20)
    assert group_discount(20, True) == 40

def test_group_discount_school_large_above():
    # Branch: is_school -> True, group_size >= 20 -> True (above: 35)
    assert group_discount(35, True) == 40

def test_group_discount_school_small_boundary():
    # Branch: is_school -> True, group_size >= 20 -> False (boundary: 19)
    assert group_discount(19, True) == 25

def test_group_discount_school_small_minimum():
    # Branch: is_school -> True, group_size >= 20 -> False (minimum: 1)
    assert group_discount(1, True) == 25

def test_group_discount_regular_tier1_boundary():
    # Branch: is_school -> False, group_size >= 15 -> True (boundary: 15)
    assert group_discount(15, False) == 20

def test_group_discount_regular_tier1_above():
    # Branch: is_school -> False, group_size >= 15 -> True (above: 25)
    assert group_discount(25, False) == 20

def test_group_discount_regular_tier2_upper_boundary():
    # Branch: is_school -> False, group_size < 15 and group_size >= 8 -> True (boundary: 14)
    assert group_discount(14, False) == 10

def test_group_discount_regular_tier2_lower_boundary():
    # Branch: is_school -> False, group_size < 15 and group_size >= 8 -> True (boundary: 8)
    assert group_discount(8, False) == 10

def test_group_discount_regular_no_discount_upper_boundary():
    # Branch: is_school -> False, group_size < 8 -> False (boundary: 7)
    assert group_discount(7, False) == 0

def test_group_discount_regular_no_discount_lower_boundary():
    # Branch: is_school -> False, group_size < 8 -> False (boundary: 1)
    assert group_discount(1, False) == 0


# --- gallery_entry() Branch Coverage Tests ---

def test_gallery_entry_at_capacity_boundary():
    # Branch: visitors_inside >= capacity -> True (boundary: 100 == 100)
    assert gallery_entry(100, 100, False) == "wait"

def test_gallery_entry_over_capacity():
    # Branch: visitors_inside >= capacity -> True (above: 110 > 100)
    assert gallery_entry(110, 100, True) == "wait"

def test_gallery_entry_queue_exact_ninety_percent():
    # Branch: visitors_inside < capacity, 90% reached (90 * 10 >= 100 * 9 is True) AND not has_timed_slot (True)
    assert gallery_entry(90, 100, False) == "queue"

def test_gallery_entry_queue_above_ninety_percent():
    # Branch: visitors_inside < capacity, 95% reached AND not has_timed_slot (True)
    assert gallery_entry(95, 100, False) == "queue"

def test_gallery_entry_timed_slot_bypasses_queue_exact_ninety():
    # Branch: visitors_inside * 10 >= capacity * 9 is True BUT has_timed_slot is True (short-circuit False branch)
    # Visitors with timed slot are allowed to enter even when gallery is >= 90% full
    assert gallery_entry(90, 100, True) == "enter"

def test_gallery_entry_timed_slot_bypasses_queue_ninety_five():
    # Branch: visitors_inside * 10 >= capacity * 9 is True BUT has_timed_slot is True
    assert gallery_entry(95, 100, True) == "enter"

def test_gallery_entry_under_ninety_percent_boundary():
    # Branch: visitors_inside * 10 >= capacity * 9 is False (boundary: 89 < 90) without slot
    assert gallery_entry(89, 100, False) == "enter"

def test_gallery_entry_well_below_capacity():
    # Branch: visitors_inside * 10 >= capacity * 9 is False with slot
    assert gallery_entry(30, 100, True) == "enter"
