#### **Proposal: Improving Developer Insight Accuracy & Depth**

Current state: There is a toggle to switch between "Standard" and "Deep" analysis. It encapsulates the two possible interpretations of the problem statement. Specifically the phrase "... language/technology from the list of repos". Simple mode assumes "list of repos" means the list of repository details available in the response to user's profile request, while deep mode assumes it means the list of all repositories under the user's account even if they are not listed in the response to user's profile request. 

We have identified three areas where technical choices significantly impact the user experience. We request design guidance on the following:

| Feature Area | Suggested Approach | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Tech Stack Definition** | Incorporate **GitHub Topics** (tags like `react`, `fastapi`) alongside Languages. | Provides a modern view of the stack including frameworks, not just base languages. | Topics are voluntary; some users may have empty lists despite having deep expertise. |
| **"Top Language" Logic** | Transition from "Repo Count" to **"Total Byte Count"** when Deep Analysis is active. | Reflects the actual volume of code written (e.g., one huge Java project vs. 10 tiny Shell scripts). | Computationally more expensive; results may change drastically between "Standard" and "Deep" modes. |
| **Rate Limit UX** | Replace the "Partial Results" warning with **Progressive Loading** or a **"Login to see more"** CTA. | Reduces user frustration with API limits and provides a clear path to get better results (auth). | Requires more complex frontend state management to handle staggered data arrival. |

**Discussion Point**: Should the "Standard" analysis be faster/simpler, or should we prioritize accuracy even if it means longer load times?
