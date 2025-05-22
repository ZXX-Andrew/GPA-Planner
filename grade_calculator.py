class GradeCalculator:
    @staticmethod
    def calculate_current_grade(components, all_components=False):
        """Calculate the current grade based on completed components."""
        total_weight = 0
        weighted_sum = 0
        
        for component in components:
            if not component.is_variable or all_components:  # Only consider components that have been graded
                total_weight += component.weight
                weighted_sum += component.score * component.weight
        
        if total_weight == 0:
            return 0
        
        return weighted_sum / total_weight
    
    @staticmethod
    def calculate_required_score(components, target_grade):
        """Calculate the required score for remaining components."""
        current_true_grade = sum(c.score * c.weight for c in components if not c.is_variable)  / 100
        remaining_weight = sum(c.weight for c in components if c.is_variable)
        # print(target_grade, current_true_grade, remaining_weight)
        if remaining_weight == 0:
            return None  # No remaining components
        
        required_score = (target_grade - current_true_grade) / remaining_weight * 100
        return max(0, min(100, required_score))
    
    @staticmethod
    def calculate_grade_distribution(components, target_grade, remaining_components):
        """Calculate a balanced grade distribution for remaining components based on their weights."""
        current_true_grade = sum(c.score * c.weight for c in components if not c.is_variable)  / 100
        remaining_weight = sum(c.weight for c in remaining_components)
        
        if remaining_weight == 0:       
            return None
        
        # Calculate minimum required average score
        min_required = (target_grade - current_true_grade) / remaining_weight * 100
        
        if min_required > 100:
            return None  # Target grade is impossible to achieve
        
        # Calculate a single balanced distribution
        base_score = max(0, min(100, min_required))
        distribution = {comp.name: base_score for comp in remaining_components}
        
        return [distribution]  # Return as a list to maintain compatibility with existing code 