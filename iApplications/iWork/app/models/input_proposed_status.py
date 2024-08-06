from iWork.app.db import db
from iWork.app.models.input_parameters import InputParameter
from iWork.app.models.proposed_status import ProposedStatus
class InputProposedStatus(db.Model):
    ''' 
    table to map two tables - Input parameters table with Proposed Status (also referred as work type sometimes) table
    '''
    __tablename__ = "input_proposed_status"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_id = db.Column(db.ForeignKey('input_parameters_master.id'), nullable=False)
    proposed_status_id = db.Column(db.ForeignKey('proposed_status_master.id'), nullable=False)

    input = db.relationship("InputParameter")
    proposed_status = db.relationship("ProposedStatus")

    def __init__(self, name, description):
        self.name = name,
        self.descrition = description

    def json(self):
        return {
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def get_parameters_by_proposed_status_id(cls, proposed_status_id):
        results = db.session.query(
            cls.id.label("id"),
            InputParameter.id.label('input_parameter_id'),
            InputParameter.name.label('input_parameter_name'),
            InputParameter.description.label('input_parameter_description'),
            ProposedStatus.id.label('proposed_status_id'),
            ProposedStatus.proposed_status.label('proposed_status')
        ).join(InputParameter, InputParameter.id == cls.input_id
        ).join(ProposedStatus, ProposedStatus.id == cls.proposed_status_id
        ).filter(ProposedStatus.id == proposed_status_id).all()

        if results:
            parameters = [
                {
                    'id': result.input_parameter_id,
                    'input_parameter_name': result.input_parameter_name,
                    'input_parameter_description': result.input_parameter_description,
                    'proposed_status_id': result.proposed_status_id,
                    'proposed_status': result.proposed_status
                }
                for result in results
            ]
            return parameters
        else:
            return None