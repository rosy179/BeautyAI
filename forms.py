from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, FloatField, IntegerField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Nhập email của bạn'})
    password = PasswordField('Mật khẩu', validators=[DataRequired()], render_kw={'placeholder': 'Nhập mật khẩu'})

class RegisterForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=3, max=20)], render_kw={'placeholder': 'Tên đăng nhập'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email của bạn'})
    full_name = StringField('Họ và tên', validators=[DataRequired()], render_kw={'placeholder': 'Họ và tên đầy đủ'})
    phone = StringField('Số điện thoại', validators=[Optional()], render_kw={'placeholder': 'Số điện thoại'})
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)], render_kw={'placeholder': 'Mật khẩu (ít nhất 6 ký tự)'})
    password2 = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Nhập lại mật khẩu'})

class SkinAnalysisForm(FlaskForm):
    skin_image = FileField('Ảnh khuôn mặt', validators=[
        DataRequired('Vui lòng chọn ảnh'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Chỉ chấp nhận file ảnh JPG, JPEG, PNG')
    ])
    age = IntegerField('Tuổi', validators=[Optional(), NumberRange(min=13, max=100)], render_kw={'placeholder': 'Tuổi của bạn'})
    skin_concerns = SelectField('Mối quan tâm về da', choices=[
        ('acne', 'Mụn trứng cá'),
        ('wrinkles', 'Nếp nhăn'),
        ('dark_spots', 'Đốm đen'),
        ('dryness', 'Da khô'),
        ('oiliness', 'Da dầu'),
        ('sensitivity', 'Da nhạy cảm'),
        ('other', 'Khác')
    ], validators=[Optional()])

class ProductForm(FlaskForm):
    name = StringField('Tên sản phẩm', validators=[DataRequired()], render_kw={'placeholder': 'Tên sản phẩm'})
    description = TextAreaField('Mô tả', render_kw={'placeholder': 'Mô tả chi tiết sản phẩm'})
    price = FloatField('Giá', validators=[DataRequired(), NumberRange(min=0)], render_kw={'placeholder': 'Giá sản phẩm'})
    brand = StringField('Thương hiệu', render_kw={'placeholder': 'Thương hiệu'})
    category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])
    stock_quantity = IntegerField('Số lượng', validators=[NumberRange(min=0)], render_kw={'placeholder': 'Số lượng trong kho'})
    skin_type = SelectField('Loại da phù hợp', choices=[
        ('all', 'Mọi loại da'),
        ('oily', 'Da dầu'),
        ('dry', 'Da khô'),
        ('combination', 'Da hỗn hợp'),
        ('sensitive', 'Da nhạy cảm'),
        ('normal', 'Da thường')
    ])
    ingredients = TextAreaField('Thành phần', render_kw={'placeholder': 'Thành phần chính của sản phẩm'})
    image_url = StringField('URL hình ảnh', render_kw={'placeholder': 'URL của ảnh sản phẩm'})

class ReviewForm(FlaskForm):
    rating = SelectField('Đánh giá', choices=[(5, '5 sao - Tuyệt vời'), (4, '4 sao - Tốt'), (3, '3 sao - Bình thường'), (2, '2 sao - Kém'), (1, '1 sao - Rất kém')], coerce=int, validators=[DataRequired()])
    title = StringField('Tiêu đề', validators=[DataRequired()], render_kw={'placeholder': 'Tiêu đề đánh giá'})
    content = TextAreaField('Nội dung', validators=[DataRequired()], render_kw={'placeholder': 'Chia sẻ trải nghiệm của bạn về sản phẩm này'})

class BlogPostForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()], render_kw={'placeholder': 'Tiêu đề bài viết'})
    excerpt = TextAreaField('Tóm tắt', render_kw={'placeholder': 'Tóm tắt ngắn gọn về bài viết'})
    content = TextAreaField('Nội dung', validators=[DataRequired()], render_kw={'placeholder': 'Nội dung bài viết'})
    featured_image = StringField('Ảnh đại diện', render_kw={'placeholder': 'URL ảnh đại diện cho bài viết'})
    tags = StringField('Tags', render_kw={'placeholder': 'skincare, makeup, beauty (phân cách bằng dấu phẩy)'})
    is_published = BooleanField('Xuất bản ngay')

class CheckoutForm(FlaskForm):
    full_name = StringField('Họ và tên', validators=[DataRequired()], render_kw={'placeholder': 'Họ và tên người nhận'})
    phone = StringField('Số điện thoại', validators=[DataRequired()], render_kw={'placeholder': 'Số điện thoại người nhận'})
    address = TextAreaField('Địa chỉ', validators=[DataRequired()], render_kw={'placeholder': 'Địa chỉ giao hàng chi tiết'})
    payment_method = SelectField('Phương thức thanh toán', choices=[
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('momo', 'Ví MoMo'),
        ('zalopay', 'ZaloPay')
    ], validators=[DataRequired()])
    notes = TextAreaField('Ghi chú', render_kw={'placeholder': 'Ghi chú đặc biệt (nếu có)'})

class ChatForm(FlaskForm):
    message = TextAreaField('Tin nhắn', validators=[DataRequired()], render_kw={'placeholder': 'Nhập câu hỏi của bạn về làm đẹp...'})
