# -*- coding: utf-8 -*-

import os
from django.conf import settings

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from reportlab.lib.pagesizes import letter


def create_fights_pdf(user, tournament_name, history_fights):
    pdf_dir = os.path.join(settings.MEDIA_ROOT)

    if user:
        path = os.path.join(pdf_dir, 'users', user.first_name + " " + user.last_name, 'walki.pdf')
    else:
        path = os.path.join(pdf_dir, 'pdf', 'walki.pdf')

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Header", fontSize=12, alignment=0))
    styles.add(ParagraphStyle(name="Strong", fontSize=10, alignment=0))

    doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=18, leftMargin=18, topMargin=18, bottomMargin=18)

    story = [Paragraph(u'Nazwa turnieju: %s' % tournament_name, styles["Header"]), Spacer(1, 30)]

    if history_fights:
        for round in history_fights:
            story.append(Spacer(1, 20))
            story.append(Paragraph(u'Runda %d' % round, styles["Strong"]))

            for fights in history_fights[round]:
                story.append(Spacer(1, 10))

                fighter_one = fights[0].return_full_name() if fights[0] else None
                fighter_two = fights[1].return_full_name() if fights[1] else None

                if fighter_one and fighter_two:
                    story.append(Paragraph("AKA: " + fighter_one + " vs. " + "AO: " + fighter_two, styles["Strong"]))
                elif fighter_one and not fighter_two:
                    story.append(Paragraph(u'WINNER: ' + fighter_one, styles["Strong"]))
                elif not fighter_one and fighter_two:
                    story.append(Paragraph(u'WINNER: ' + fighter_two, styles["Strong"]))

    doc.build(story)