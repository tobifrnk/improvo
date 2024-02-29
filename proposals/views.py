import hashlib
import user_agents
from django.db.models import F
from django.utils.encoding import smart_bytes
from django.shortcuts import render, redirect, get_object_or_404

from .models import Proposal, Comment, Upvote


def proposals(request):
    proposals = Proposal.objects.all()
    return render(request, "all_proposals.html", {"proposals": proposals})


def proposal_details(request, id):
    error_message = None
    proposal = Proposal.objects.get(id=id)
    comments = Comment.objects.filter(proposal=proposal)

    upvote_count = proposal.upvotes.count()

    if request.method == "POST":
        author = request.POST.get("Author")
        text = request.POST.get("Text")

        if author and text:
            proposal = get_object_or_404(Proposal, id=id)
            Comment.objects.create(author=author, text=text, proposal=proposal)
        else:
            error_message = "Author and/or text required!"

    return render(
        request,
        "proposal_details.html",
        {
            "proposal": proposal,
            "comments": comments,
            "error_message": error_message,
            "upvote_count": upvote_count,
        },
    )


def proposal_submission(request):
    categories = Proposal.CATEGORY_CHOICES
    error_message = None

    if request.method == "POST":
        title = request.POST.get("Title")
        proposal_content = request.POST.get("Proposal")
        category = request.POST.get("Category")

        if title and proposal_content and category:
            Proposal.objects.create(
                title=title, content=proposal_content, category=category
            )
            return redirect("index")
        else:
            error_message = "Category, title, and/or proposal content are required."

    return render(
        request,
        "proposal_submission.html",
        {"categories": categories, "error_message": error_message},
    )


def upvote_proposal(request, proposal_id):
    if request.method == "POST":
        proposal = get_object_or_404(Proposal, id=proposal_id)
        upvote_count = proposal.upvotes.count()
        comments = Comment.objects.filter(proposal=proposal)

        user_agent_string = request.META.get("HTTP_USER_AGENT", "")
        user_agent_string = user_agents.parse(user_agent_string)
        browser_fingerprint = hashlib.md5(smart_bytes(user_agent_string)).hexdigest()

        if Upvote.objects.filter(
            proposal=proposal, browser_fingerprint=browser_fingerprint
        ).exists():
            error_message = "You have already upvoted this proposal."
            return render(
                request,
                "proposal_details.html",
                {
                    "proposal": proposal,
                    "error_message": error_message,
                    "upvote_count": upvote_count,
                    "comments": comments,
                },
            )

        else:
            proposal.upvotes_count = F("upvotes_count") + 1
            proposal.save()
            Upvote.objects.create(
                proposal=proposal, browser_fingerprint=browser_fingerprint
            )

        return redirect("proposal_details", id=proposal_id)


def index(request):
    return render(request, "index.html")
