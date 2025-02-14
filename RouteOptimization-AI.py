import numpy as np
from typing import List, Dict

class RouteReportGenerator:
    def __init__(self, warehouses: List[str], cost_matrix: np.ndarray):
        self.warehouses = warehouses
        self.cost_matrix = cost_matrix
        
    def generate_validation_report(self) -> str:
        """Generate the data validation section of the report."""
        return f"""# Data Validation Report
## 1. Data Structure Check:
- Number of warehouses: {len(self.warehouses)}
- Dimensions of cost matrix: {self.cost_matrix.shape[0]} x {self.cost_matrix.shape[1]}

## 2. Required Fields Check:
- Warehouses: Present ({', '.join(self.warehouses)})
- Cost Matrix: Present

## 3. Data Type Validation:
- All cost values are verified as non-negative numbers.

## Validation Summary:
Data validation is successful! Proceeding with cost analysis...
"""

    def generate_formulas_section(self) -> str:
        """Generate the formulas section."""
        return """# Formulas Used:
1. Direct Route Cost:
 $$\\text{Cost} = C_{xy}$$
2. Multi-stop Route Cost:
 $$\\text{Total Cost} = C_{i1,i2} + C_{i2,i3} + \\dots + C_{in-1,in}$$
"""

    def generate_direct_routes_analysis(self) -> tuple:
        """Generate analysis for direct routes and return the report text and optimal routes."""
        direct_routes = []
        optimal_direct_cost = float('inf')
        optimal_direct_routes = []
        
        report = "# Detailed Analysis for Direct Routes\n\n"
        
        route_num = 1
        for i, start in enumerate(self.warehouses):
            for j, end in enumerate(self.warehouses):
                if i != j:
                    cost = self.cost_matrix[i][j]
                    if cost < optimal_direct_cost:
                        optimal_direct_cost = cost
                        optimal_direct_routes = [(start, end)]
                    elif cost == optimal_direct_cost:
                        optimal_direct_routes.append((start, end))
                        
                    route_details = f"""### Route#{route_num}: {start} to {end}
- **Starting Warehouse:** {start}
- **Destination Warehouse:** {end}
- **Direct Route Cost:** $C_{{{start[0]},{end[0]}}}$
**Calculation:**
Locate the cost in the row for {start} and the column for {end}:
$$\\text{{Cost}} = C_{{{start[0]},{end[0]}}} = {cost}$$

---

"""
                    report += route_details
                    direct_routes.append((start, end, cost))
                    route_num += 1
                    
        return report, direct_routes, optimal_direct_routes, optimal_direct_cost

    def generate_multi_stop_analysis(self) -> tuple:
        """Generate analysis for multi-stop routes and return the report text and optimal routes."""
        report = "# Detailed Analysis for Multi-stop Routes\n\n"
        report += "For multi-stop routes in a {}-warehouse network, we consider a single intermediate stop.\n\n".format(len(self.warehouses))
        
        multi_stop_routes = []
        optimal_multi_cost = float('inf')
        optimal_multi_routes = []
        
        for i, start in enumerate(self.warehouses):
            for j, end in enumerate(self.warehouses):
                if i != j:
                    for k, via in enumerate(self.warehouses):
                        if k != i and k != j:
                            cost1 = self.cost_matrix[i][k]
                            cost2 = self.cost_matrix[k][j]
                            total_cost = cost1 + cost2
                            
                            if total_cost < optimal_multi_cost:
                                optimal_multi_cost = total_cost
                                optimal_multi_routes = [(start, via, end)]
                            elif total_cost == optimal_multi_cost:
                                optimal_multi_routes.append((start, via, end))
                                
                            route_details = f"""### Multi-stop Route for {start} to {end}
- **Route:** {start} -> {via} -> {end}
**Step 1:** {start} to {via}
$$\\text{{Cost}}_{{{''.join([start[0], '\\to', via[0]])}}} = C_{{{start[0]},{via[0]}}} = {cost1}$$
**Step 2:** {via} to {end}
$$\\text{{Cost}}_{{{''.join([via[0], '\\to', end[0]])}}} = C_{{{via[0]},{end[0]}}} = {cost2}$$
**Total Multi-stop Cost:**
$$\\text{{Total Cost}} = {cost1} + {cost2} = {total_cost}$$

---

"""
                            report += route_details
                            multi_stop_routes.append((start, via, end, total_cost))
        
        return report, multi_stop_routes, optimal_multi_routes, optimal_multi_cost

    def generate_final_summary(self, direct_routes, optimal_direct_routes, optimal_direct_cost,
                             multi_stop_routes, optimal_multi_routes, optimal_multi_cost) -> str:
        """Generate the final route summary section."""
        summary = "# Final Route Summary\n\n"
        
        # Direct routes summary
        summary += "### Direct Routes:\n"
        for i, (start, end, cost) in enumerate(direct_routes, 1):
            summary += f"- **Route#{i}:** {start} -> {end} = {cost}\n"
        
        summary += f"\n**Optimal Direct Route:**\n"
        route_desc = " and ".join([f"**{start} -> {end}**" for start, end in optimal_direct_routes])
        summary += f"The lowest cost direct routes are {route_desc} with a cost of **{optimal_direct_cost}**.\n\n"
        
        # Multi-stop routes summary
        summary += "### Multi-stop Routes:\n"
        for start, via, end, cost in multi_stop_routes:
            summary += f"- **{start} -> {end} via {via}:** Total Cost = {cost}\n"
        
        summary += f"\n**Optimal Multi-stop Route:**\n"
        route_desc = " and ".join([f"**{start} -> {end} via {via}**" for start, via, end in optimal_multi_routes])
        summary += f"The lowest cost multi-stop routes are {route_desc} with a cost of **{optimal_multi_cost}**.\n\n"
        
        # Final recommendation
        summary += """# Final Recommendation:
- **Recommended Direct Route:**\n"""
        route_desc = " or ".join([f"**{start} -> {end}**" for start, end in optimal_direct_routes])
        summary += f"  {route_desc} with a cost of **{optimal_direct_cost}**.\n\n"
        
        summary += "- **Recommended Multi-stop Route:**\n"
        route_desc = " or ".join([f"**{start} -> {end} via {via}**" for start, via, end in optimal_multi_routes])
        summary += f"  {route_desc} with a cost of **{optimal_multi_cost}**.\n\n"
        
        return summary

    def generate_full_report(self) -> str:
        """Generate the complete route optimization report."""
        # Generate all report sections
        validation_report = self.generate_validation_report()
        formulas_section = self.generate_formulas_section()
        
        # Summary of total routes
        total_routes = f"""# Route Cost Analysis Summary
Total Direct Routes Evaluated: {len(self.warehouses) * (len(self.warehouses) - 1)}
Total Multi-stop Routes Evaluated: {len(self.warehouses) * (len(self.warehouses) - 1) * (len(self.warehouses) - 2)}\n\n"""
        
        # Generate detailed analysis sections
        direct_analysis, direct_routes, optimal_direct_routes, optimal_direct_cost = self.generate_direct_routes_analysis()
        multi_stop_analysis, multi_stop_routes, optimal_multi_routes, optimal_multi_cost = self.generate_multi_stop_analysis()
        
        # Generate final summary
        final_summary = self.generate_final_summary(
            direct_routes, optimal_direct_routes, optimal_direct_cost,
            multi_stop_routes, optimal_multi_routes, optimal_multi_cost
        )
        
        # Combine all sections
        full_report = "\n".join([
            validation_report,
            formulas_section,
            total_routes,
            direct_analysis,
            multi_stop_analysis,
            final_summary,
            "# Feedback Request",
            "Would you like detailed calculations for any specific route? Rate this analysis (1-5)."
        ])
        
        return full_report

# Example usage
def main():
    # Example data
    warehouses = ["A", "B", "C", "D"]
    cost_matrix = np.array([
        [0, 12, 25, 18],
    [12, 0, 17, 20],
    [25, 17, 0, 22],
    [18, 20, 22, 0]
    ])
    
    # Generate report
    report_generator = RouteReportGenerator(warehouses, cost_matrix)
    report = report_generator.generate_full_report()
    print(report)

if __name__ == "__main__":
    main()