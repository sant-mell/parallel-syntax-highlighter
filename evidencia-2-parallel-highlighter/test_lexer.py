"""Tests for the DFA lexer (lexer_dfa.lexer_python).

Run with: pytest
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexer_dfa


def _tokenize(source):
    """Write source to a temp .py file and return the lexer's segments."""
    fd, path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(source)
        return lexer_dfa.lexer_python(path)
    finally:
        os.unlink(path)


def test_returns_lexema_tipo_tuples():
    segments = _tokenize("x = 42\n")
    assert isinstance(segments, list) and segments
    for segment in segments:
        assert isinstance(segment, tuple) and len(segment) == 2


def test_lossless_reconstruction():
    # The lexer appends a trailing newline when the input lacks one.
    source = "n = 10\nname = \"hi\"\n# comment\n"
    segments = _tokenize(source)
    reconstructed = "".join(lexema for lexema, _ in segments)
    assert reconstructed == source


def test_css_classes_for_basic_tokens():
    segments = _tokenize('total = 42 + count  # note\nmsg = "hello"\n')
    classes = {lexer_dfa.clase_css(tipo) for _, tipo in segments}
    assert {"numero", "identificador", "operador", "comentario", "cadena"} <= classes
