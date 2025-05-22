import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QLineEdit, QPushButton,
                            QComboBox, QSpinBox, QDoubleSpinBox, QTabWidget,
                            QScrollArea, QGroupBox, QFileDialog, QSlider,
                            QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt
import pandas as pd
from grade_calculator import GradeCalculator

class CourseComponent:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.score = 0.0
        self.is_variable = True # Flag to indicate if the component is variable

class Course:
    def __init__(self, name):
        self.name = name
        self.components = []
        self.target_grade = 0.0

class GPAPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPA Planner")
        self.setMinimumSize(800, 600)
        
        # Initialize data
        self.courses = []
        self.current_course = None
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Create tabs
        self.course_setup_tab = QWidget()
        self.grade_input_tab = QWidget()
        self.planning_tab = QWidget()
        
        tabs.addTab(self.course_setup_tab, "Course Setup")
        tabs.addTab(self.grade_input_tab, "Grade Input")
        tabs.addTab(self.planning_tab, "Score Planning")
        
        self.setup_course_tab()
        self.setup_grade_tab()
        self.setup_planning_tab()
        
        # Connect signals
        self.course_select.currentIndexChanged.connect(self.update_grade_input)
        self.planning_course_select.currentIndexChanged.connect(self.update_planning)
        self.target_grade_input.valueChanged.connect(self.update_planning)
    
    def setup_course_tab(self):
        layout = QVBoxLayout(self.course_setup_tab)
        
        # Course name input
        course_name_layout = QHBoxLayout()
        course_name_label = QLabel("Course Name:")
        self.course_name_input = QLineEdit()
        course_name_layout.addWidget(course_name_label)
        course_name_layout.addWidget(self.course_name_input)
        layout.addLayout(course_name_layout)
        
        # Component setup
        component_group = QGroupBox("Course Components")
        component_layout = QVBoxLayout()
        
        # Add component button
        add_component_btn = QPushButton("Add Component")
        add_component_btn.clicked.connect(self.add_component)
        component_layout.addWidget(add_component_btn)
        
        # Components list
        self.components_layout = QVBoxLayout()
        component_layout.addLayout(self.components_layout)
        
        component_group.setLayout(component_layout)
        layout.addWidget(component_group)
        
        # Save course button
        save_course_btn = QPushButton("Save Course")
        save_course_btn.clicked.connect(self.save_course)
        layout.addWidget(save_course_btn)
    
    def setup_grade_tab(self):
        layout = QVBoxLayout(self.grade_input_tab)
        
        # Course selection
        course_select_layout = QHBoxLayout()
        course_select_label = QLabel("Select Course:")
        self.course_select = QComboBox()
        course_select_layout.addWidget(course_select_label)
        course_select_layout.addWidget(self.course_select)
        layout.addLayout(course_select_layout)
        
        # Grade input area
        self.grade_input_group = QGroupBox("Grade Input")
        self.grade_input_layout = QVBoxLayout()
        self.grade_input_group.setLayout(self.grade_input_layout)
        layout.addWidget(self.grade_input_group)
        
        # Import grades button
        import_btn = QPushButton("Import Grades")
        import_btn.clicked.connect(self.import_grades)
        layout.addWidget(import_btn)
    
    def setup_planning_tab(self):
        layout = QVBoxLayout(self.planning_tab)
        
        # Course selection
        course_select_layout = QHBoxLayout()
        course_select_label = QLabel("Select Course:")
        self.planning_course_select = QComboBox()
        course_select_layout.addWidget(course_select_label)
        course_select_layout.addWidget(self.planning_course_select)
        layout.addLayout(course_select_layout)
        
        # Target grade input
        target_grade_layout = QHBoxLayout()
        target_grade_label = QLabel("Target Grade:")
        self.target_grade_input = QDoubleSpinBox()
        self.target_grade_input.setRange(0, 100)
        self.target_grade_input.setValue(0)  # Set default to 0
        target_grade_layout.addWidget(target_grade_label)
        target_grade_layout.addWidget(self.target_grade_input)
        layout.addLayout(target_grade_layout)
        
        # Current grade display
        self.current_grade_label = QLabel("Current Grade: N/A")
        layout.addWidget(self.current_grade_label)
        
        # Predicted grade display
        self.predicted_grade_label = QLabel("Predicted Grade: N/A")
        layout.addWidget(self.predicted_grade_label)
        
        # Planning area
        self.planning_group = QGroupBox("Score Planning")
        self.planning_layout = QVBoxLayout()
        self.planning_group.setLayout(self.planning_layout)
        layout.addWidget(self.planning_group)
    
    def add_component(self):
        component_layout = QHBoxLayout()
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Component Name")
        
        weight_input = QDoubleSpinBox()
        weight_input.setRange(0, 100)
        weight_input.setValue(20)
        weight_input.setSuffix("%")
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.remove_component(component_layout))
        
        component_layout.addWidget(name_input)
        component_layout.addWidget(weight_input)
        component_layout.addWidget(remove_btn)
        
        self.components_layout.addLayout(component_layout)
    
    def remove_component(self, component_layout):
        while component_layout.count():
            item = component_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def save_course(self):
        course_name = self.course_name_input.text()
        if not course_name:
            QMessageBox.warning(self, "Error", "Please enter a course name")
            return
        
        # Check if total weight is 100%
        total_weight = 0
        for i in range(self.components_layout.count()):
            component_layout = self.components_layout.itemAt(i).layout()
            if component_layout:
                weight_input = component_layout.itemAt(1).widget()
                if weight_input:
                    total_weight += weight_input.value()
        
        if abs(total_weight - 100) > 0.01:
            QMessageBox.warning(self, "Error", "Total weight must equal 100%")
            return
        
        course = Course(course_name)
        
        # Get components
        for i in range(self.components_layout.count()):
            component_layout = self.components_layout.itemAt(i).layout()
            if component_layout:
                name_input = component_layout.itemAt(0).widget()
                weight_input = component_layout.itemAt(1).widget()
                
                if name_input and weight_input:
                    component = CourseComponent(
                        name_input.text(),
                        weight_input.value()
                    )
                    course.components.append(component)
        
        self.courses.append(course)
        self.update_course_lists()
        
        # Clear inputs
        self.course_name_input.clear()
        while self.components_layout.count():
            item = self.components_layout.takeAt(0)
            if item.layout():
                self.remove_component(item.layout())
    
    def update_course_lists(self):
        self.course_select.clear()
        self.planning_course_select.clear()
        
        for course in self.courses:
            self.course_select.addItem(course.name)
            self.planning_course_select.addItem(course.name)
    
    def update_grade_input(self):
        # Clear existing grade inputs
        while self.grade_input_layout.count():
            item = self.grade_input_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get selected course
        index = self.course_select.currentIndex()
        if index < 0:
            return
        
        course = self.courses[index]
        
        # Create grade inputs for each component
        for component in course.components:
            component_layout = QHBoxLayout()
            
            name_label = QLabel(component.name)
            
            # Add checkbox for is_variable
            variable_checkbox = QCheckBox("Variable in Calculations")
            
            variable_checkbox.setChecked(component.is_variable)
            variable_checkbox.stateChanged.connect(
                lambda state, c=component: self.update_component_variable(c, state)
            )
            
            score_input = QDoubleSpinBox()
            score_input.setRange(0, 100)
            score_input.setDecimals(2)  # Set precision to 2 decimal places
            score_input.setValue(component.score)
            score_input.valueChanged.connect(
                lambda value, c=component, vc=variable_checkbox: self.update_component_score(c, vc, value)
            )
            
            
            
            component_layout.addWidget(name_label)
            component_layout.addWidget(score_input)
            component_layout.addWidget(variable_checkbox)
            
            self.grade_input_layout.addLayout(component_layout)
    
    def update_component_score(self, component, variable_checkbox, score):
        component.score = score
        if score > 0:  # Only set is_variable to true if there's a score
            component.is_variable = False
            variable_checkbox = variable_checkbox.setChecked(component.is_variable)
        self.update_planning()
    
    def update_component_variable(self, component, state):
        component.is_variable = (state == Qt.CheckState.Checked.value)
        self.update_planning()
    
    def import_grades(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import Grades",
            "",
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        )
        
        if not file_name:
            return
        
        try:
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_name)
            else:
                df = pd.read_excel(file_name)
            
            # TODO: Implement grade import logic
            QMessageBox.information(self, "Success", "Grades imported successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import grades: {str(e)}")
    
    def update_planning(self):
        # Clear existing planning widgets
        while self.planning_layout.count():
            item = self.planning_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Reset predicted grade display
        self.predicted_grade_label.setText("Predicted Grade: N/A")
        
        # Get selected course
        index = self.planning_course_select.currentIndex()
        if index < 0:
            return
        
        course = self.courses[index]
        target_grade = self.target_grade_input.value()
        
        # Calculate current grade
        current_grade = GradeCalculator.calculate_current_grade(course.components)
        self.current_grade_label.setText(f"Current Grade: {current_grade:.2f}%")
        
        # Get remaining components (those that haven't been graded)
        remaining_components = [c for c in course.components if c.is_variable]
        
        if not remaining_components:
            QMessageBox.information(self, "Info", "No remaining components to plan")
            return
        
        # Calculate required scores
        if len(remaining_components) == 1:
            # Single component - show slider
            component = remaining_components[0]
            required_score = GradeCalculator.calculate_required_score(
                course.components,
                target_grade
            )
            
            if required_score is None:
                QMessageBox.warning(self, "Warning", "Target grade is impossible to achieve")
                return
            
            # Create a container widget for the slider section
            slider_container = QWidget()
            slider_container_layout = QVBoxLayout(slider_container)
            
            # Add slider
            slider_layout = QHBoxLayout()
            slider_label = QLabel(f"{component.name} Required Score:")
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 10000)  # Use larger range for better precision
            slider.setValue(int(required_score * 100))  # Scale up for precision
            slider_value = QLabel(f"{required_score:.2f}%")
            
            def update_predicted_grade(value):
                # Convert slider value to actual score (0-100)
                actual_score = value / 100.0
                # Calculate predicted grade based on slider value
                component.score = actual_score
                
                predicted_grade = GradeCalculator.calculate_current_grade(course.components, True)
                # print('OVO',predicted_grade)
                self.predicted_grade_label.setText(f"Predicted Grade: {predicted_grade:.2f}%")
                slider_value.setText(f"{actual_score:.2f}%")
            
            slider.valueChanged.connect(update_predicted_grade)
            
            slider_layout.addWidget(slider_label)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(slider_value)
            
            slider_container_layout.addLayout(slider_layout)
            self.planning_layout.addWidget(slider_container)
            
            # Initial predicted grade calculation
            update_predicted_grade(int(required_score * 100))
            
        else:
            # Multiple components - show possible distributions
            distributions = GradeCalculator.calculate_grade_distribution(
                course.components,
                target_grade,
                remaining_components
            )
            
            if not distributions:
                QMessageBox.warning(self, "Warning", "Target grade is impossible to achieve")
                return
            
            # Show possible distributions
            for i, distribution in enumerate(distributions[:3]):  # Show top 3 distributions
                dist_container = QWidget()
                dist_layout = QVBoxLayout(dist_container)
                
                dist_label = QLabel(f"Option {i+1}:")
                dist_layout.addWidget(dist_label)
                
                # Calculate predicted grade for this distribution
                for comp in remaining_components:
                    comp.score = distribution[comp.name]
                predicted_grade = GradeCalculator.calculate_current_grade(course.components)
                
                for component, score in distribution.items():
                    comp_layout = QHBoxLayout()
                    comp_label = QLabel(f"{component}:")
                    score_label = QLabel(f"{score:.2f}%")
                    comp_layout.addWidget(comp_label)
                    comp_layout.addWidget(score_label)
                    dist_layout.addLayout(comp_layout)
                
                # Add predicted grade for this distribution
                pred_label = QLabel(f"Predicted Grade: {predicted_grade:.2f}%")
                dist_layout.addWidget(pred_label)
                
                self.planning_layout.addWidget(dist_container)
                
                # Reset component scores after calculation
                for comp in remaining_components:
                    comp.score = 0.0

def main():
    app = QApplication(sys.argv)
    window = GPAPlanner()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 