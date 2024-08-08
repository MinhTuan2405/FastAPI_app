Để nhúng một câu lệnh SQL thô vào SQLAlchemy, bạn có thể sử dụng phương thức `text()` từ SQLAlchemy để thực thi câu lệnh đó. Dưới đây là một ví dụ về cách thực hiện điều này:

### 1. Thiết lập cơ sở dữ liệu và bảng mẫu

Giả sử bạn đã thiết lập cơ sở dữ liệu và bảng mẫu như sau:

```python
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)
```

### 2. Sử dụng `text()` để thực thi câu lệnh SQL thô

Bạn có thể sử dụng `text()` để thực thi câu lệnh SQL thô và lấy kết quả như sau:

```python
from sqlalchemy import text
from sqlalchemy.orm import Session

# Tạo phiên làm việc
db = SessionLocal()

# Câu lệnh SQL thô
sql_query = text("SELECT * FROM users")

# Thực thi câu lệnh SQL thô
result = db.execute(sql_query)

# Lấy tất cả các hàng
rows = result.fetchall()

# In kết quả
for row in rows:
    print(row)
```

### 3. Chuyển đổi kết quả sang các đối tượng ORM

Nếu bạn muốn chuyển đổi kết quả của câu lệnh SQL thô sang các đối tượng ORM của SQLAlchemy, bạn có thể làm như sau:

```python
# Thực thi câu lệnh SQL thô
result = db.execute(sql_query)

# Chuyển đổi kết quả thành các đối tượng ORM
users = [User(**row) for row in result.mappings()]

# In kết quả
for user in users:
    print(user.id, user.name)
```

### Tổng kết

Dưới đây là toàn bộ ví dụ từ đầu đến cuối, bao gồm cả thiết lập cơ sở dữ liệu và bảng mẫu, thực thi câu lệnh SQL thô, và chuyển đổi kết quả thành các đối tượng ORM:

```python
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Tạo phiên làm việc
db = SessionLocal()

# Câu lệnh SQL thô
sql_query = text("SELECT * FROM users")

# Thực thi câu lệnh SQL thô
result = db.execute(sql_query)

# Chuyển đổi kết quả thành các đối tượng ORM
users = [User(**row) for row in result.mappings()]

# In kết quả
for user in users:
    print(user.id, user.name)
```

Với cách này, bạn có thể dễ dàng nhúng các câu lệnh SQL thô vào SQLAlchemy và tận dụng các tính năng ORM của nó.