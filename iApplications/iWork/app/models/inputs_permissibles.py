from iWork.app.db import db
from iWork.app.models import InputParameter, PermissibleWork

class InputAndPermissible(db.Model):
    ''' 
    table to map two tables - Input parameters table with Proposed Status (also referred as work type sometimes) table
    '''
    __tablename__ = "inputs_and_permissibles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_parameter_id = db.Column(db.ForeignKey('input_parameters.id'), nullable=False)
    permissible_work_id = db.Column(db.ForeignKey('nrega_permissible_works.id'), nullable=False)

    input = db.relationship("InputParameter")
    permissible_work = db.relationship("PermissibleWork")

    def __init__(self, name, description):
        self.name = name,
        self.descrition = description

    def json(self):
        return {
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def get_parameters_by_permissible_work_id(cls, permissible_work_id):
        results = db.session.query(
            cls.id.label("id"),
            InputParameter.id.label('input_parameter_id'),
            InputParameter.name.label('input_parameter_name'),
            InputParameter.description.label('input_parameter_description'),
            InputParameter.label.label('input_parameter_label'),
            InputParameter.unit.label('input_parameter_unit'),
            InputParameter.element_type.label('element_type'),
            PermissibleWork.id.label('permissible_work_id'),
            PermissibleWork.permissible_work.label('permissible_work')
        ).join(InputParameter, InputParameter.id == cls.input_parameter_id
        ).join(PermissibleWork, PermissibleWork.id == cls.permissible_work_id
        ).filter(PermissibleWork.id == permissible_work_id).all()

        if results:
            parameters = [
                {
                    'id': result.input_parameter_id,
                    'name': result.input_parameter_name,
                    'description': result.input_parameter_description,
                    'label':result.input_parameter_label,
                    'unit':result.input_parameter_unit,
                    'element_type':result.element_type,
                    'permissible_work_id': result.permissible_work_id,
                    'permissible_work': result.permissible_work
                }
                for result in results
            ]
            return parameters
        else:
            return None