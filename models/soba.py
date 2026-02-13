from database import db

class Soba(db.Model):
    __tablename__ = 'soba'

    id_sobe = db.Column(db.Integer, primary_key = True)

    igrac1_id = db.Column(db.Integer, db.ForeignKey('igrac.id'), nullable=False)
    igrac2_id = db.Column(db.Integer, db.ForeignKey('igrac.id'), nullable=False)
    igrac3_id = db.Column(db.Integer, db.ForeignKey('igrac.id'), nullable=False)
    igrac4_id = db.Column(db.Integer, db.ForeignKey('igrac.id'), nullable=False)

    pobjede_tim_mi = db.Column(db.Integer, default=0)
    pobjede_tim_vi = db.Column(db.Integer, default=0)


    def __repr__(self):
        return f"<Soba {self.id_sobe}: Mi {self.pobjede_tim_mi} - Vi {self.pobjede_tim_vi}>"
    

