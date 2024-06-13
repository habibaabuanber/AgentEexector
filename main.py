from graphs.super_graph import super_graph
from langchain_core.messages import HumanMessage
import os

# Entry point to run the multi-agent system

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TAVILY_API_KEY = os.environ['TAVILY_API_KEY']

if __name__ == "__main__":
    for s in super_graph.stream(
        {
            "messages": [
                HumanMessage(
                    content=
                    """File Name: 1. project/src/components/Offerings/index.js

Detailed Page Description
Page Title: Offerings
Purpose
The Offerings page is designed to showcase the various services, talents, and capabilities that our company offers. This page serves as a comprehensive presentation to potential clients and stakeholders, highlighting our expertise and the value we can provide.

Design
Layout
Header: A prominent header at the top of the page, featuring the company's logo and a navigation menu.
Hero Section: Below the header, a hero section with a high-quality background image or video that encapsulates the essence of our offerings. This section includes a headline and a brief introductory paragraph.
Main Content: The main content area is divided into several sections, each highlighting a specific service or capability.
Service Sections: Each service section includes:
Service Title: A bold, clear title for the service.
Service Description: A detailed description of what the service entails.
Icons/Images: Relevant icons or images that visually represent the service.
Key Benefits: A list of key benefits or unique selling points of the service.
Talent Showcase: A dedicated section to showcase the talents within the company, including:
Profile Cards: Individual cards for each team member, featuring:
Profile Picture: A professional photo.
Name: Full name of the team member.
Role: The role or title of the team member.
Bio: A short bio highlighting their expertise and contributions.
Call to Action (CTA): A prominent CTA section encouraging visitors to contact us, request a consultation, or view case studies.
Footer: The footer includes contact information, social media links, and quick navigation links to other important sections of the website.

Color Scheme and Typography
Color Scheme: A professional and cohesive color palette that aligns with the company's branding. Primary colors for headers and CTAs, secondary colors for backgrounds, and neutral colors for text.
Typography: Clean and readable fonts for headings, subheadings, and body text. Emphasis on readability and a modern aesthetic.

Functionality
Responsive Design: The page is fully responsive, ensuring a seamless experience across all devices, from desktops to mobile phones.
Interactive Elements:
Hover Effects: Icons and images with subtle hover effects to enhance user engagement.
Expandable Sections: Service descriptions that can expand to show more details on click.
Profile Modal: Clicking on a team member's profile card opens a modal with a more detailed bio and links to their professional profiles (e.g., LinkedIn).
Accessibility: The page is designed with accessibility in mind, featuring alt text for images, ARIA labels for interactive elements, and high contrast for readability.
SEO Optimization: The page is optimized for search engines with relevant keywords, meta descriptions, and structured data to improve visibility.
""")
            ],
        },
        {"recursion_limit": 150},
    ):
        if "__end__" not in s:
            print(s)
            print("---")
