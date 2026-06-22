from __future__ import annotations

from testgen.rag.quality import assess_rag_quality


def test_rag_quality_missing_when_no_chunks():
    quality = assess_rag_quality(
        {
            "docs": {"top_k_requested": 4, "returned_chunks": 0, "sources": []},
            "source": {"top_k_requested": 4, "returned_chunks": 0, "sources": []},
        }
    )

    assert quality["verdict"] == "missing"
    assert quality["score"] == 0
    assert quality["returned_chunks"] == 0


def test_rag_quality_low_score_sets_low_confidence():
    quality = assess_rag_quality(
        {
            "docs": {
                "returned_chunks": 1,
                "sources": [
                    {
                        "score": 0.12,
                        "metadata_missing_fields": [],
                    }
                ],
            },
            "source": {"returned_chunks": 0, "sources": []},
        },
        min_confidence=0.35,
    )

    assert quality["verdict"] == "weak"
    assert quality["low_confidence"] is True
    assert any("low relevance" in warning for warning in quality["warnings"])


def test_rag_quality_warns_when_metadata_missing():
    quality = assess_rag_quality(
        {
            "docs": {
                "returned_chunks": 1,
                "sources": [
                    {
                        "score": 0.82,
                        "metadata_missing_fields": ["section", "line_start"],
                    }
                ],
            }
        }
    )

    assert quality["verdict"] == "weak"
    assert quality["missing_metadata_count"] == 1
    assert any("metadata" in warning for warning in quality["warnings"])


def test_rag_quality_pytest_ast_context_skip_is_not_warning():
    quality = assess_rag_quality(
        {
            "docs": {"returned_chunks": 0, "sources": []},
            "source": {
                "returned_chunks": 0,
                "sources": [],
                "skipped_reason": "pytest_ast_context",
            },
        }
    )

    assert quality["verdict"] == "missing"
    assert quality["groups"]["source"]["skipped_reason"] == "pytest_ast_context"
    assert quality["warnings"] == []


def test_rag_quality_good_when_scores_and_metadata_are_ok():
    quality = assess_rag_quality(
        {
            "docs": {
                "returned_chunks": 2,
                "sources": [
                    {"score": 0.77, "metadata_missing_fields": []},
                    {"score": 0.66, "metadata_missing_fields": []},
                ],
            },
            "source": {"returned_chunks": 0, "sources": []},
        }
    )

    assert quality["verdict"] == "good"
    assert quality["score"] >= 70
    assert quality["warnings"] == []


def test_rag_quality_avg_score_uses_all_scored_chunks():
    quality = assess_rag_quality(
        {
            "docs": {
                "returned_chunks": 2,
                "sources": [
                    {"score": 0.9, "metadata_missing_fields": []},
                    {"score": 0.5, "metadata_missing_fields": []},
                ],
            },
            "source": {
                "returned_chunks": 1,
                "sources": [
                    {"score": 0.7, "metadata_missing_fields": []},
                ],
            },
        }
    )

    assert quality["avg_score"] == 0.7
    assert quality["max_score"] == 0.9
