# visualization.py

import matplotlib.pyplot as plt
import os
import textwrap

def generate_recommendation_plot(club, clubs, club_scores):
    # Ensure club_scores is a dictionary, providing a default if None
    if club_scores is None:
        club_scores = {}

    # Filter out clubs with no score and sort
    clubs_with_scores = [c for c in clubs if c["name"] in club_scores]
    sorted_clubs = sorted(clubs_with_scores, key=lambda c: club_scores.get(c["name"], 0.0), reverse=True)
    
    # Take top 10 for clarity, or all if fewer than 10
    top_clubs = sorted_clubs[:10]
    
    # Wrap long club names
    club_names = [textwrap.fill(c["name"], 35) for c in top_clubs]
    scores = [club_scores.get(c["name"], 0.0) for c in top_clubs]

    # Assign colors: a special color for the recommended club
    recommended_color = '#10B981'  # Emerald Green
    default_color = '#60A5FA'     # Soft Blue
    colors = [recommended_color if c["name"] == club else default_color for c in top_clubs]
    
    # Reverse the lists so the highest score is at the top of the plot
    club_names.reverse()
    scores.reverse()
    colors.reverse()

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(club_names, scores, color=colors, height=0.6)
    
    # Add titles and labels with better fonts
    ax.set_title("Classement des Clubs Recommandés", fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel("Score de Compatibilité", fontsize=12)
    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='x', labelsize=10)
    
    # Set x-axis limits to be consistent (0 to 1 for similarity score)
    ax.set_xlim(0, 1.05)
    
    # Remove plot spines for a cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add score labels on each bar for clarity
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.01,
            bar.get_y() + bar.get_height() / 2,
            f'{width:.2f}',
            ha='left',
            va='center',
            fontsize=10,
            fontweight='bold'
        )

    plt.tight_layout()
    
    os.makedirs("static/plots", exist_ok=True)
    # Use a more unique name to prevent browser caching issues
    safe_club_name = "".join(x for x in club if x.isalnum())
    plot_path = f"static/plots/recommendation_{safe_club_name}.png"
    plt.savefig(plot_path, format="png", dpi=150)
    plt.close()
    return plot_path