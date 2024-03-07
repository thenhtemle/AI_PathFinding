Đây là file chứa class Graph, đại diện cho biểu đồ hiện tại
Có các hàm public là: 
1) Hàm tạo: nhận 2 tham số là tên file input và tên thuật toán được sử dụng
2) Hàm expand: nhận 1 tham số là cặp số (tuple) x, y chứa vị trí muốn expand. Hàm trả về 2 mảng: các vị trí đã được expand và các vị trí đã ở frontier.
Hàm có thể không trả gì nếu đã tìm thấy đích. Lúc đó, hàm này sẽ output ra kết quả. 
Hàm throw exception nếu vị trí đó đã được expanded.
Hàm mặc định gắn parent của các đỉnh của mảng trả về đầu tiên là vị trí truyền vào tham số.
2.5) Hàm expand: không nhận tham số: khi đó hàm sẽ expand đỉnh đầu và vẫn trả về 2 mảng các vị trí đã được expand
3) Hàm heuristic: nhận 1 tham số là cặp số (tuple) x, y muốn tìm giá trị heuristic, là khoảng cách Mahattan giữa điểm đó và điểm đích
4) Hàm give_up (lul): không nhận tham số, chỉ sử dụng khi chắc chắn là không tồn tại đường đi
5) Hàm get_width: trả về chiều dài và chiều rộng của đồ thị
6) Hàm get_start: trả về điểm bắt đầu của đồ thị
7) Hàm get_goal: trả về điểm đích của đồ thị
8) Hàm set_parent: nhận 2 tham số là vị trí cần thay đổi pos và giá trị thay đổi par. Khi đó, đỉnh trước pos sẽ được chỉnh thành par

Có thể tham khảo file DFS.py để hiểu hơn cách sử dụng...