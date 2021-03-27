#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Move to the next line and show a text string, using a w as the word spacing
    and a c as the character spacing (setting the corresponding parameters in
    the text state). a w and a c shall be numbers expressed in unscaled text
    space units.
"""
import typing
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetSpacingMoveToNextLineShowText(CanvasOperator):
    """
    Move to the next line and show a text string, using a w as the word spacing
    and a c as the character spacing (setting the corresponding parameters in
    the text state). a w and a c shall be numbers expressed in unscaled text
    space units. This operator shall have the same effect as this code:
    aw Tw
    ac Tc
    string '
    """

    def __init__(self):
        super().__init__('"', 3)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        """
        Invoke the " operator
        """
        set_word_spacing_op: typing.Optional[CanvasOperator] = canvas.get_operator("Tw")
        assert set_word_spacing_op
        set_word_spacing_op.invoke(canvas, [operands[0]])

        set_character_spacing_op: typing.Optional[CanvasOperator] = canvas.get_operator(
            "Tc"
        )
        assert set_character_spacing_op
        set_character_spacing_op.invoke(canvas, [operands[1]])

        move_to_next_line_show_text_op: typing.Optional[
            CanvasOperator
        ] = canvas.get_operator("'")
        assert move_to_next_line_show_text_op
        move_to_next_line_show_text_op.invoke(canvas, [operands[2]])
