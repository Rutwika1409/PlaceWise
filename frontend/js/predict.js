document
.getElementById("predictionForm")
.addEventListener(
    "submit",
    async function (e) {

        e.preventDefault();

        const payload = {

            cgpa: parseFloat(
                document.getElementById("cgpa").value
            ),

            branch:
                document.getElementById("branch").value,

            backlogs: parseInt(
                document.getElementById("backlogs").value
            ),

            internships_count: parseInt(
                document.getElementById(
                    "internships_count"
                ).value
            ),

            projects_count: parseInt(
                document.getElementById(
                    "projects_count"
                ).value
            ),

            coding_skill_score: parseFloat(
                document.getElementById(
                    "coding_skill_score"
                ).value
            ),

            mock_interview_score: parseFloat(
                document.getElementById(
                    "mock_interview_score"
                ).value
            ),

            logical_reasoning_score: parseFloat(
                document.getElementById(
                    "logical_reasoning_score"
                ).value
            ),

            communication_skill_score: parseFloat(
                document.getElementById(
                    "communication_skill_score"
                ).value
            ),

            aptitude_score: parseFloat(
                document.getElementById(
                    "aptitude_score"
                ).value
            ),

            leadership_score: parseFloat(
                document.getElementById(
                    "leadership_score"
                ).value
            ),

            extracurricular_score: parseFloat(
                document.getElementById(
                    "extracurricular_score"
                ).value
            )
        };

        // Validate payload - branch is string, others are numbers
        if (!payload.branch || payload.branch.trim() === "") {
            alert("Please select a branch.");
            return;
        }

        for (const key in payload) {
            if (key === "branch") continue; // Skip branch as it's a string
            if (isNaN(payload[key]) || payload[key] === "") {
                alert(`Please fill all fields with valid numbers. ${key} is invalid.`);
                return;
            }
        }

        try {

            console.log("Sending prediction request with payload:", payload);

            const response =
                await fetch(
                    "/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                );

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const result =
                await response.json();

            console.log("Prediction result received:", result);

            document.getElementById(
                "probability"
            ).innerHTML =
                `<strong>Placement Probability:</strong>
                 ${result.placement_probability}%`;

            document.getElementById(
                "status"
            ).innerHTML =
                `<strong>Status:</strong>
                 ${result.placement_status}`;

            const gapList =
                document.getElementById(
                    "skillGaps"
                );

            gapList.innerHTML = "";

            if (result.skill_gaps && Array.isArray(result.skill_gaps)) {
                result.skill_gaps.forEach(
                    gap => {

                        gapList.innerHTML +=
                            `<li>${gap}</li>`;
                    }
                );
            }

            const recommendationList =
                document.getElementById(
                    "recommendations"
                );

            recommendationList.innerHTML = "";

            if (result.recommendation && result.recommendation.actionable_insights) {
                result.recommendation
                    .actionable_insights
                    .forEach(
                        insight => {

                            recommendationList.innerHTML +=
                                `<li>${insight}</li>`;
                        }
                    );
            }

            if (result.recommendation && result.recommendation.final_recommendation) {
                document.getElementById(
                    "finalRecommendation"
                ).innerHTML =
                    `<strong>Final Recommendation:</strong> ${result.recommendation.final_recommendation}`;
            }

            console.log("Prediction display completed successfully.");

        }

        catch(error) {

            console.error("Prediction error:", error);

            alert(
                "Prediction failed: " + error.message + ". Please check the console for details."
            );
        }

    }
);