from app import db
import enum

class LevelEnum(enum.Enum):
	A,B,C,D,E,F = "A","B","C","D","E","F"

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)

class Timeseries(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	blarg = db.Column(db.Float)
	level = db.Column(db.String(1))
	mean = db.Column(db.Float)
	std = db.Column(db.Float)

	def serialize(self):
		return {
			'id': self.id,
			'blarg': self.blarg,
			'level': self.level,
			'mean': self.mean,
			'std': self.std
		}
		

	def __repr__(self):
		return '<Timeseries %r %r %r %r %r>' % (self.id, self.blarg, self.level,self.mean,self.std)
