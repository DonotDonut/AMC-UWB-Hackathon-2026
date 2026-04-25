import random
import pandas as pd
import matplotlib.pyplot as plt

from machine_learning.eclat import EclatScheduleSuggestion


class EclatTest: 
    @staticmethod
    def validate_eclat_results(
        frequent_df,
        suggestions_df,
        output_prefix="output data/eclat_validation"
    ):
        # -----------------------------
        # 1. Basic validation metrics
        # -----------------------------
        validation_summary = {
            "total_frequent_patterns": len(frequent_df),
            "total_schedule_suggestions": len(suggestions_df),
            "unique_events": suggestions_df["event_name"].nunique(),
            "unique_stores": suggestions_df["store_name"].nunique(),
            "unique_employees": suggestions_df["employee_id"].nunique(),
            "avg_distance_to_event": suggestions_df["distance_to_event_miles"].mean(),
        }

        summary_df = pd.DataFrame(
            list(validation_summary.items()),
            columns=["Metric", "Value"]
        )

        # -----------------------------
        # 2. Top frequent Eclat patterns
        # -----------------------------
        top_patterns = frequent_df.sort_values(
            by="support",
            ascending=False
        ).head(15)

        # -----------------------------
        # 3. Suggestions by crowd rank
        # -----------------------------
        crowd_rank_counts = suggestions_df["crowd_rank"].value_counts().reset_index()
        crowd_rank_counts.columns = ["crowd_rank", "suggestion_count"]

        # -----------------------------
        # 4. Suggestions by position
        # -----------------------------
        position_counts = suggestions_df["position"].value_counts().reset_index()
        position_counts.columns = ["position", "suggestion_count"]

        # -----------------------------
        # 5. Save validation workbook
        # -----------------------------
        excel_output = f"{output_prefix}.xlsx"

        with pd.ExcelWriter(excel_output) as writer:
            summary_df.to_excel(writer, sheet_name="Validation Summary", index=False)
            top_patterns.to_excel(writer, sheet_name="Top Eclat Patterns", index=False)
            crowd_rank_counts.to_excel(writer, sheet_name="By Crowd Rank", index=False)
            position_counts.to_excel(writer, sheet_name="By Position", index=False)

        print(f"Saved validation workbook: {excel_output}")

        # -----------------------------
        # 6. Plot top Eclat patterns
        # -----------------------------
        plt.figure(figsize=(12, 6))
        plt.barh(top_patterns["itemset"], top_patterns["support"])
        plt.xlabel("Support Count")
        plt.ylabel("Frequent Pattern")
        plt.title("Top Eclat Frequent Patterns")
        plt.gca().invert_yaxis()
        plt.tight_layout()

        pattern_plot = f"{output_prefix}_top_patterns.png"
        plt.savefig(pattern_plot)
        plt.close()

        # -----------------------------
        # 7. Plot suggestions by crowd rank
        # -----------------------------
        plt.figure(figsize=(8, 5))
        plt.bar(crowd_rank_counts["crowd_rank"], crowd_rank_counts["suggestion_count"])
        plt.xlabel("Crowd Rank")
        plt.ylabel("Schedule Suggestions")
        plt.title("Schedule Suggestions by Crowd Rank")
        plt.tight_layout()

        crowd_plot = f"{output_prefix}_crowd_rank.png"
        plt.savefig(crowd_plot)
        plt.close()

        # -----------------------------
        # 8. Plot suggestions by position
        # -----------------------------
        plt.figure(figsize=(10, 5))
        plt.bar(position_counts["position"], position_counts["suggestion_count"])
        plt.xlabel("Position")
        plt.ylabel("Schedule Suggestions")
        plt.title("Schedule Suggestions by Position")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        position_plot = f"{output_prefix}_position.png"
        plt.savefig(position_plot)
        plt.close()

        print(f"Saved plots:")
        print(pattern_plot)
        print(crowd_plot)
        print(position_plot)

        return summary_df

    @staticmethod
    def validate_train_test_patterns(
        transactions,
        min_support=3,
        test_size=0.30,
        output_prefix="output data/eclat_train_test_validation"
    ):
        transactions = transactions.copy()
        random.shuffle(transactions)

        split_index = int(len(transactions) * (1 - test_size))

        train_transactions = transactions[:split_index]
        test_transactions = transactions[split_index:]

        train_patterns = EclatScheduleSuggestion.run_eclat(
            train_transactions,
            min_support=min_support
        )

        test_patterns = EclatScheduleSuggestion.run_eclat(
            test_transactions,
            min_support=min_support
        )

        train_set = set(train_patterns.keys())
        test_set = set(test_patterns.keys())
        overlapping_patterns = train_set & test_set

        summary_df = pd.DataFrame([
            {"Metric": "Train Transactions", "Value": len(train_transactions)},
            {"Metric": "Test Transactions", "Value": len(test_transactions)},
            {"Metric": "Train Frequent Patterns", "Value": len(train_patterns)},
            {"Metric": "Test Frequent Patterns", "Value": len(test_patterns)},
            {"Metric": "Overlapping Patterns", "Value": len(overlapping_patterns)},
            {
                "Metric": "Pattern Overlap Rate",
                "Value": round(len(overlapping_patterns) / len(train_set), 4)
                if len(train_set) > 0 else 0
            }
        ])

        comparison_df = pd.DataFrame([
            {"Dataset": "Train", "Frequent Pattern Count": len(train_patterns)},
            {"Dataset": "Test", "Frequent Pattern Count": len(test_patterns)},
            {"Dataset": "Overlap", "Frequent Pattern Count": len(overlapping_patterns)}
        ])

        train_df = pd.DataFrame([
            {
                "transaction_id": i + 1,
                "items": ", ".join(sorted(transaction))
            }
            for i, transaction in enumerate(train_transactions)
        ])

        test_df = pd.DataFrame([
            {
                "transaction_id": i + 1,
                "items": ", ".join(sorted(transaction))
            }
            for i, transaction in enumerate(test_transactions)
        ])

        train_patterns_df = pd.DataFrame([
            {
                "itemset": ", ".join(itemset),
                "support": support
            }
            for itemset, support in train_patterns.items()
        ])

        test_patterns_df = pd.DataFrame([
            {
                "itemset": ", ".join(itemset),
                "support": support
            }
            for itemset, support in test_patterns.items()
        ])

        excel_output = f"{output_prefix}.xlsx"

        with pd.ExcelWriter(excel_output) as writer:
            summary_df.to_excel(writer, sheet_name="Train Test Summary", index=False)
            comparison_df.to_excel(writer, sheet_name="Pattern Comparison", index=False)
            train_df.to_excel(writer, sheet_name="Training Transactions", index=False)
            test_df.to_excel(writer, sheet_name="Testing Transactions", index=False)
            train_patterns_df.to_excel(writer, sheet_name="Train Patterns", index=False)
            test_patterns_df.to_excel(writer, sheet_name="Test Patterns", index=False)

        plt.figure(figsize=(8, 5))
        plt.bar(
            comparison_df["Dataset"],
            comparison_df["Frequent Pattern Count"]
        )
        plt.xlabel("Dataset")
        plt.ylabel("Frequent Pattern Count")
        plt.title("Eclat Train vs Test Pattern Comparison")
        plt.tight_layout()

        plot_output = f"{output_prefix}_comparison.png"
        plt.savefig(plot_output)
        plt.close()

        print(f"Saved train/test validation workbook: {excel_output}")
        print(f"Saved train/test comparison plot: {plot_output}")

        return summary_df, comparison_df, train_df, test_df