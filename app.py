import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from utils.data_loader import load_graph_data
from algorithms.dijkstra import dijkstra, get_shortest_path
from algorithms.bfs import bfs, reconstruct_path
from algorithms.prim import prim
import folium
from streamlit_folium import folium_static
import random
import numpy as np

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Lập kế hoạch Tuyến đường Du lịch Việt Nam",
    page_icon="🇻🇳",
    layout="wide"
)

# Tải dữ liệu đồ thị
def load_data():
    # Dữ liệu đồ thị (được cung cấp trong đề bài)
    graph = {'Chau Doc': [['Cantho', 90], ['Ho Chi Minh City', 320]], 
         'Phu Yen': [['Binh Dinh', 100], ['Khanh Hoa', 120]], 
         'Thai Binh': [['Hanoi', 100]], 
         'Muong Lay': [['Dien Bien Phu', 105], ['Sapa', 200]], 
         'Phong Nha Cave': [['Quang Binh', 50]], 
         'Son La': [['Dien Bien Phu', 200], ['Mai Chau', 190]], 
         'Khanh Hoa': [['Ninh Thuan', 80], ['Phu Yen', 120]], 
         'Tay Trang frontière': [['Dien Bien Phu', 38]], 
         'Mai Chau': [['Hanoi', 200], ['Na Meo frontière', 150], ['Ninh Binh', 200], ['Son La', 190]], 
         'Mui Ke Ga': [['Binh Thuan', 40]], 
         'Moc Bai': [['Tay Ninh', 55]], 
         'Hai Phong': [['Quang Ninh', 50], ['Thanh Hoa', 150]], 
         'Ninh Thuan': [['Binh Thuan', 100], ['Khanh Hoa', 80]], 
         'Dong Van Karst Plateau': [['Ha Giang', 150]], 
         'Hung Yen': [['Hanoi', 50]], 
         'Hoi An': [['Cu Lao Cham', 20], ['Danang', 35], ['Phuoc Son', 160], ['Quinhon', 280]], 
         'Hoa Binh': [['Hanoi', 80]], 
         'Thai Nguyen': [['Hanoi', 80]], 
         'Cantho': [['Chau Doc', 90], ['Ho Chi Minh City', 230], ['Rach Gia', 90], ['Vinh Long', 45]], 
         'Phu Tho': [['Hanoi', 90]], 
         'Rach Gia': [['Cantho', 90], ['Phu Quoc', 120]], 
         'Hue': [['Da Nang', 100], ['Danang', 130], ['Dong Hoi', 190], ['Quang Tri', 70]], 
         'Tra Vinh': [['Ben Tre', 50], ['Soc Trang', 60]],
         'Binh Thuan': [['Dong Nai', 150], ['Mui Ke Ga', 40], ['Ninh Thuan', 100]], 
         'Tay Ninh': [['Cu Chi', 50], ['Ho Chi Minh City', 100], ['Moc Bai', 55]], 
         'Buon Ma Thuot': [['Kontum', 250], ['Lac Lak', 50]], 
         'Dalat': [['Ho Chi Minh City', 340], ['Lac Lak', 220], ['Mui Ne', 180], ['Nha Trang', 240]], 
         'Hanoi': [['Bac Giang', 50], ['Bac Ninh', 40], ['Ha Giang', 300], ['Hai Duong', 60], ['Halong', 160], ['Hoa Binh', 80], ['Hung Yen', 50], ['Mai Chau', 200], ['Nam Dinh', 90], ['Ninh Binh', 100], ['Phu Tho', 90], ['Sapa', 400], ['Thai Binh', 100], ['Thai Nguyen', 80], ['Vinh', 330], ['Vinh Phuc', 60]], 
         'Bac Ha': [['Lao Cai', 100]], 
         'Bac Lieu': [['Ca Mau', 80], ['Soc Trang', 70]], 
         'Binh Duong': [['Ho Chi Minh City', 30]], 
         'Ba Na Hills': [['Da Nang', 30]], 
         'Quang Tri': [['Hue', 70], ['Quang Binh', 80]], 
         'Ben Tre': [['Long An', 70], ['Tra Vinh', 50]], 
         'Soc Trang': [['Bac Lieu', 70], ['Tra Vinh', 60]], 
         'Ho Chi Minh City': [['Binh Duong', 30], ['Cantho', 230], ['Chau Doc', 320], ['Cu Chi', 50], ['Dalat', 340], ['Dong Nai', 50], ['Dong Thap', 150], ['Hau Giang', 200], ['Long An', 60], ['Mui Ne', 220], ['My Tho', 95], ['Tay Ninh', 100], ['Vinh Long', 180]],
         'Nghe An': [['Ha Tinh', 100], ['Thanh Hoa', 150]], 
         'Binh Dinh': [['Phu Yen', 100], ['Quang Ngai', 150]], 
         'Quinhon': [['Hoi An', 280], ['Nha Trang', 250]], 
         'Sapa': [['Hanoi', 400], ['Lao Cai', 38], ['Muong Lay', 200]], 
         'Ha Giang': [['Cao Bang', 150], ['Dong Van Karst Plateau', 150], ['Hanoi', 300]],
         'Kien Giang': [['Ca Mau', 100]], 
         'Kontum': [['Buon Ma Thuot', 250], ['Phuoc Son', 220]], 
         'Danang': [['Hoi An', 35], ['Hue', 130]], 
         'Na Meo frontière': [['Mai Chau', 150]],
         'Lang Son': [['Cao Bang', 120], ['Quang Ninh', 100]], 
         'Phuoc Son': [['Hoi An', 160], ['Kontum', 220]],
         'My Tho': [['Ho Chi Minh City', 95]],
         'Bac Giang': [['Hanoi', 50]], 
         'Thanh Hoa': [['Hai Phong', 150], ['Nghe An', 150]], 
         'Dong Thap': [['Ho Chi Minh City', 150]],
         'Ca Mau': [['Bac Lieu', 80], ['Kien Giang', 100]], 
         'Vinh': [['Dong Hoi', 200], ['Hanoi', 330]], 
         'Ha Tinh': [['Nghe An', 100], ['Quang Binh', 120]], 
         'My Lai': [['Quang Ngai', 12]], 
         'Nam Dinh': [['Hanoi', 90]], 
         'Quang Nam': [['Da Nang', 50], ['Quang Ngai', 100]],
         'Mui Ne': [['Dalat', 180], ['Ho Chi Minh City', 220], ['Nha Trang', 260]], 
         'Cu Chi': [['Ho Chi Minh City', 50], ['Tay Ninh', 50]], 
         'Vinh Phuc': [['Hanoi', 60]], 
         'Cau Treo': [['Dong Hoi', 300]], 
         'Cu Lao Cham': [['Hoi An', 20]], 
         'Dong Nai': [['Binh Thuan', 150], ['Ho Chi Minh City', 50]], 
         'Quang Binh': [['Ha Tinh', 120], ['Phong Nha Cave', 50], ['Quang Tri', 80]],
         'Halong': [['Hanoi', 160], ['Ninh Binh', 300]], 
         'Vinh Long': [['Cantho', 45], ['Ho Chi Minh City', 180]], 
         'Hai Duong': [['Hanoi', 60]],
         'Long An': [['Ben Tre', 70], ['Ho Chi Minh City', 60]], 
         'Quang Ngai': [['Binh Dinh', 150], ['My Lai', 12], ['Quang Nam', 100]], 
         'Bac Ninh': [['Hanoi', 40]], 
         'Quang Ninh': [['Hai Phong', 50], ['Lang Son', 100]], 
         'Dong Hoi': [['Cau Treo', 300], ['Hue', 190], ['Vinh', 200]], 
         'Ninh Binh': [['Halong', 300], ['Hanoi', 100], ['Mai Chau', 200]],
         'Lao Cai': [['Bac Ha', 100], ['Sapa', 38]],
         'Cao Bang': [['Ha Giang', 150], ['Lang Son', 120]], 
         'Da Nang': [['Ba Na Hills', 30], ['Hue', 100], ['Quang Nam', 50]], 
         'Phu Quoc': [['Rach Gia', 120]], 
         'Lac Lak': [['Buon Ma Thuot', 50], ['Dalat', 220]], 
         'Nha Trang': [['Dalat', 240], ['Mui Ne', 260], ['Quinhon', 250]], 
         'Hau Giang': [['Ho Chi Minh City', 200]], 
         'Dien Bien Phu': [['Muong Lay', 105], ['Son La', 200], ['Tay Trang frontière', 38]]
    }

    # Dữ liệu tọa độ (được cung cấp trong đề bài)
    coordinates = {
        'Chau Doc': (105.1, 10.7167),
        'Cantho': (105.7667, 10.0333),
        'Ho Chi Minh City': (106.6297, 10.8231),
        'Phu Yen': (109.2, 13.0833),
        'Binh Dinh': (109.2, 13.7833),
        'Khanh Hoa': (109.1872, 12.2583),
        'Thai Binh': (106.3333, 20.4500),
        'Muong Lay': (103.1333, 22.0667),
        'Phong Nha Cave': (106.3167, 17.5500),
        'Son La': (103.9167, 21.3333),
        'Tay Trang frontière': (102.9667, 21.6333),
        'Mai Chau': (105.0833, 20.6667),
        'Mui Ke Ga': (108.1667, 10.7333),
        'Moc Bai': (106.0, 11.0667),
        'Hai Phong': (106.6833, 20.8667),
        'Ninh Thuan': (108.9833, 11.5667),
        'Dong Van Karst Plateau': (105.1333, 23.2833),
        'Hung Yen': (106.0667, 20.65),
        'Hoi An': (108.3380, 15.8800),
        'Hoa Binh': (105.3333, 20.8167),
        'Thai Nguyen': (105.8333, 21.5833),
        'Phu Tho': (105.2167, 21.4),
        'Rach Gia': (105.0833, 10.0167),
        'Hue': (107.5833, 16.4667),
        'Tra Vinh': (106.35, 9.9333),
        'Binh Thuan': (108.1, 10.9333),
        'Tay Ninh': (106.1, 11.3),
        'Buon Ma Thuot': (108.05, 12.6667),
        'Dalat': (108.4333, 11.9333),
        'Hanoi': (105.8342, 21.0278),
        'Bac Ha': (104.3, 22.5333),
        'Bac Lieu': (105.7333, 9.2833),
        'Binh Duong': (106.6667, 11.1667),
        'Ba Na Hills': (108.0, 15.9667),
        'Quang Tri': (107.2, 16.75),
        'Ben Tre': (106.3833, 10.2333),
        'Soc Trang': (105.9667, 9.6),
        'Nghe An': (105.6833, 18.6667),
        'Quinhon': (109.2333, 13.7667),
        'Sapa': (103.8667, 22.3500),
        'Ha Giang': (104.9833, 22.8333),
        'Kien Giang': (105.1167, 10.0),
        'Kontum': (108.0, 14.35),
        'Danang': (108.2, 16.0667),
        'Na Meo frontière': (105.4667, 20.25),
        'Lang Son': (106.7667, 21.85),
        'Phuoc Son': (107.8333, 15.4),
        'My Tho': (106.35, 10.35),
        'Bac Giang': (106.2, 21.2667),
        'Thanh Hoa': (105.7667, 19.8),
        'Dong Thap': (105.6667, 10.45),
        'Ca Mau': (105.15, 9.1833),
        'Vinh': (105.6833, 18.6667),
        'Ha Tinh': (105.9, 18.3333),
        'My Lai': (108.8333, 15.1333),
        'Nam Dinh': (106.1667, 20.4167),
        'Quang Nam': (108.0167, 15.5333),
        'Mui Ne': (108.1, 10.9333),
        'Cu Chi': (106.5, 10.9667),
        'Vinh Phuc': (105.6, 21.3167),
        'Cau Treo': (105.75, 18.0833),
        'Cu Lao Cham': (108.5, 15.9333),
        'Dong Nai': (106.8167, 10.95),
        'Quang Binh': (106.6, 17.4667),
        'Halong': (107.0667, 20.95),
        'Vinh Long': (105.9667, 10.25),
        'Hai Duong': (106.3167, 20.9333),
        'Long An': (106.4167, 10.5333),
        'Quang Ngai': (108.8, 15.1167),
        'Bac Ninh': (106.05, 21.1833),
        'Quang Ninh': (107.0667, 20.95),
        'Dong Hoi': (106.6167, 17.4833),
        'Ninh Binh': (105.9667, 20.25),
        'Lao Cai': (103.9667, 22.4833),
        'Cao Bang': (106.25, 22.6667),
        'Da Nang': (108.2, 16.0667),
        'Phu Quoc': (103.9667, 10.2167),
        'Lac Lak': (108.1833, 12.4167),
        'Nha Trang': (109.1833, 12.25),
        'Hau Giang': (105.4667, 9.7833),
        'Dien Bien Phu': (103.0167, 21.3833)
    }
    
    # Tải dữ liệu đồ thị
    travel_graph = load_graph_data(graph, coordinates)
    return travel_graph, coordinates

# Tạo đồ thị NetworkX để hiển thị
def create_networkx_graph(graph):
    G = nx.DiGraph()
    
    # Thêm các nút
    for location_name, location in graph.vertices.items():
        if location.coordinates:
            G.add_node(location_name, pos=location.coordinates)
        else:
            G.add_node(location_name)
    
    # Thêm các cạnh
    for from_location, neighbors in graph.edges.items():
        for to_location, distance in neighbors:
            G.add_edge(from_location, to_location, weight=distance)
    
    return G

# Hiển thị đồ thị sử dụng matplotlib
def visualize_graph_matplotlib(G, path=None, zoom_on_path=False):
    plt.figure(figsize=(15, 10))
    pos = nx.get_node_attributes(G, 'pos')
    
    if zoom_on_path and path:
        # Chỉ hiển thị các nút trong đường đi và các nút lân cận
        path_set = set(path)
        neighbors_set = set()
        
        # Thêm các nút lân cận của các nút trong đường đi
        for node in path:
            neighbors = list(G.neighbors(node)) + list(G.predecessors(node))
            neighbors_set.update(neighbors)
        
        # Kết hợp các nút trong đường đi và các nút lân cận
        nodes_to_show = path_set.union(neighbors_set)
        
        # Tạo đồ thị con chỉ chứa các nút cần hiển thị
        subgraph = G.subgraph(nodes_to_show)
        
        # Vẽ các nút và cạnh của đồ thị con
        nx.draw_networkx_nodes(subgraph, pos, node_size=300, node_color='skyblue')
        nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.3)
        
        # Vẽ đường đi
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=500, node_color='red')
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.5, alpha=1.0, edge_color='red')
        
        # Vẽ nhãn cho các nút
        nx.draw_networkx_labels(subgraph, pos, font_size=10)
        
        # Tính toán giới hạn để zoom vào đường đi
        path_pos = [pos[node] for node in path]
        x_values = [p[0] for p in path_pos]
        y_values = [p[1] for p in path_pos]
        
        # Thêm padding để đảm bảo tất cả các nút đều hiển thị
        padding = 0.5
        x_min, x_max = min(x_values) - padding, max(x_values) + padding
        y_min, y_max = min(y_values) - padding, max(y_values) + padding
        
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
    else:
        # Vẽ tất cả các nút và cạnh
        nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.3)
        
        # Nếu có đường đi, vẽ đường đi
        if path:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=500, node_color='red')
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.5, alpha=1.0, edge_color='red')
        
        # Vẽ nhãn cho các nút
        nx.draw_networkx_labels(G, pos, font_size=8)
    
    plt.axis('off')
    return plt

# Tạo bản tóm tắt tuyến đường có thể tải xuống
def create_route_summary(path, total_distance, path_details):
    """Tạo bản tóm tắt tuyến đường có thể tải xuống"""
    summary = f"Tóm tắt Tuyến đường: {' → '.join(path)}\n"
    summary += f"Tổng Quãng đường: {total_distance} km\n\n"
    summary += "Chỉ dẫn Chi tiết:\n"
    
    for detail in path_details:
        summary += f"- {detail['Từ']} đến {detail['Đến']}: {detail['Khoảng cách (km)']} km\n"
    
    return summary

# Ứng dụng chính
def main():
    st.title("🇻🇳 Lập kế hoạch Tuyến đường Du lịch Việt Nam")
    st.write("""
    Ứng dụng giúp lập kế hoạch các tuyến đường du lịch tối ưu giữa các địa điểm khác nhau tại Việt Nam.
    """)
    
    # Thêm tên tác giả
    st.markdown("""
    <div style="text-align: right; font-style: italic; margin-bottom: 20px;">
    Tác giả: Duy - Sơn - Thuận
    </div>
    """, unsafe_allow_html=True)
    
    # Tải dữ liệu
    travel_graph, coordinates = load_data()
    
    # Tạo đồ thị NetworkX
    G = create_networkx_graph(travel_graph)
    
    # Thanh bên
    st.sidebar.title("Chọn tính năng")
    app_mode = st.sidebar.selectbox(
        "Chọn ở đây",
        ["Trang chủ", "Tìm Đường đi Ngắn nhất", "Tìm Các Địa điểm Có thể Đến", "Tìm Cây Khung Nhỏ nhất", "Khám phá Tất cả Địa điểm"]
    )
    
    # Lấy tất cả các địa điểm
    locations = sorted(travel_graph.get_all_vertices())
    
    if app_mode == "Trang chủ":
        st.header("Ứng dụng Lập kế hoạch Tuyến đường Du lịch Việt Nam")
        st.write("""
        Ứng dụng tìm tuyến đường du lịch tối ưu tại Việt Nam.
        
        ### Tính năng:
        - **Tìm Đường đi Ngắn nhất**: Tìm tuyến đường ngắn nhất giữa hai địa điểm
        - **Tìm Các Địa điểm Có thể Đến**: Khám phá tất cả các địa điểm có thể đến từ một điểm xuất phát
        - **Tìm Cây Khung Nhỏ nhất**: Tìm mạng lưới hiệu quả nhất kết nối tất cả các địa điểm
        - **Khám phá Tất cả Địa điểm**: Xem tất cả các địa điểm có sẵn trên bản đồ
        
        ### Cách sử dụng:
        1. Chọn một tính năng từ thanh bên
        2. Chọn địa điểm xuất phát và đích đến
        3. Xem kết quả và hình ảnh trực quan
        """)
        
        # Hiển thị một mẫu các địa điểm
        st.subheader("Mẫu các Địa điểm Có sẵn")
        sample_locations = random.sample(locations, min(10, len(locations)))
        st.write(", ".join(sample_locations))
        
        # Hiển thị đồ thị mạng lưới của Việt Nam
        st.subheader("Đồ thị Mạng lưới Du lịch Việt Nam")
        plt = visualize_graph_matplotlib(G)
        plt.suptitle("Mạng lưới Du lịch Việt Nam", fontsize=14)
        st.pyplot(plt)
        
    elif app_mode == "Tìm Đường đi Ngắn nhất":
        st.header("Tìm Đường đi Ngắn nhất")
        st.write("Tìm tuyến đường ngắn nhất giữa hai địa điểm tại Việt Nam.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_location = st.selectbox("Chọn địa điểm xuất phát", locations)
        
        with col2:
            end_location = st.selectbox("Chọn địa điểm đích đến", locations, index=1)
        
        if st.button("Tìm Đường đi Ngắn nhất"):
            with st.spinner("Đang tìm đường đi ngắn nhất..."):
                # Tìm đường đi ngắn nhất sử dụng thuật toán Dijkstra
                distances, parents = dijkstra(travel_graph, start_location, end_location)
                path = get_shortest_path(parents, start_location, end_location)
                
                if path:
                    st.success(f"Đã tìm thấy đường đi ngắn nhất từ {start_location} đến {end_location}!")
                    
                    # Tính tổng quãng đường
                    total_distance = 0
                    path_details = []
                    
                    for i in range(len(path) - 1):
                        for neighbor, distance in travel_graph.get_neighbors(path[i]):
                            if neighbor == path[i + 1]:
                                total_distance += distance
                                path_details.append({
                                    "Từ": path[i],
                                    "Đến": path[i + 1],
                                    "Khoảng cách (km)": distance
                                })
                                break
                    
                    # Hiển thị tóm tắt tuyến đường trong một hộp được làm nổi bật
                    st.markdown("""
                    <style>
                    .route-summary {
                        background-color: #f0f2f6;
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }
                    .total-distance {
                        font-size: 24px;
                        font-weight: bold;
                        color: #FF4B4B;
                    }
                    .route-path {
                        font-size: 18px;
                        margin-top: 10px;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="route-summary">
                        <div class="total-distance">Tổng Quãng đường: {total_distance} km</div>
                        <div class="route-path">Tuyến đường: {' → '.join(path)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hiển thị chi tiết đường đi dưới dạng bảng
                    st.subheader("Chỉ dẫn Chi tiết")
                    st.table(pd.DataFrame(path_details))
                    
                    # Hiển thị đồ thị
                    st.subheader("Hình ảnh Tuyến đường")
                    plt = visualize_graph_matplotlib(G, path, zoom_on_path=True)
                    # Thêm tiêu đề cho đồ thị
                    plt.suptitle(f"Tuyến đường: {' → '.join(path)}\nTổng Quãng đường: {total_distance} km", fontsize=12)
                    st.pyplot(plt)

                    # Thêm nút tải xuống cho bản tóm tắt tuyến đường
                    route_summary = create_route_summary(path, total_distance, path_details)
                    st.download_button(
                        label="Tải xuống Tóm tắt Tuyến đường",
                        data=route_summary,
                        file_name=f"tuyen_duong_{start_location}_den_{end_location}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Không tìm thấy đường đi từ {start_location} đến {end_location}")
        
    elif app_mode == "Tìm Các Địa điểm Có thể Đến":
        st.header("Tìm Các Địa điểm Có thể Đến")
        st.write("Khám phá tất cả các địa điểm có thể đến từ một điểm xuất phát.")
        
        start_location = st.selectbox("Chọn địa điểm xuất phát", locations)
        
        if st.button("Tìm Các Địa điểm Có thể Đến"):
            with st.spinner("Đang tìm các địa điểm có thể đến..."):
                # Tìm tất cả các địa điểm có thể đến sử dụng BFS
                parents = bfs(travel_graph, start_location)
                
                # Lấy tất cả các địa điểm có thể đến
                reachable = [loc for loc in parents.keys() if loc != start_location]
                
                if reachable:
                    st.success(f"Đã tìm thấy {len(reachable)} địa điểm có thể đến từ {start_location}!")
                    
                    # Tạo một dataframe cho các địa điểm có thể đến
                    reachable_data = []
                    
                    for location in sorted(reachable):
                        path = reconstruct_path(parents, start_location, location)
                        
                        # Tính quãng đường
                        total_distance = 0
                        for i in range(len(path) - 1):
                            for neighbor, distance in travel_graph.get_neighbors(path[i]):
                                if neighbor == path[i + 1]:
                                    total_distance += distance
                                    break
                        
                        reachable_data.append({
                            "Địa điểm": location,
                            "Khoảng cách (km)": total_distance,
                            "Đường đi": " → ".join(path)
                        })
                    
                    # Hiển thị các địa điểm có thể đến dưới dạng bảng
                    st.subheader("Các Địa điểm Có thể Đến")
                    df = pd.DataFrame(reachable_data)
                    st.dataframe(df.sort_values("Khoảng cách (km)"))
                    
                    # Hiển thị đồ thị
                    st.subheader("Đồ thị Mạng lưới")
                    plt = visualize_graph_matplotlib(G)
                    plt.suptitle(f"Các Địa điểm Có thể Đến từ {start_location}", fontsize=12)
                    st.pyplot(plt)
                else:
                    st.error(f"Không có địa điểm nào có thể đến từ {start_location}")
        
    elif app_mode == "Tìm Cây Khung Nhỏ nhất":
        st.header("Tìm Cây Khung Nhỏ nhất")
        st.write("Tìm mạng lưới hiệu quả nhất kết nối các địa điểm từ một điểm xuất phát.")
        
        start_location = st.selectbox("Chọn địa điểm xuất phát", locations)
        
        if st.button("Tìm Cây Khung Nhỏ nhất"):
            with st.spinner("Đang tìm cây khung nhỏ nhất..."):
                # Tìm cây khung nhỏ nhất sử dụng Prim
                mst = prim(travel_graph, start_location)
                
                if mst:
                    st.success(f"Đã tìm thấy cây khung nhỏ nhất từ {start_location}!")
                    
                    # Tính tổng quãng đường và tạo dữ liệu cạnh
                    total_distance = 0
                    edge_data = []
                    
                    for to_loc, from_loc in mst.items():
                        for neighbor, distance in travel_graph.get_neighbors(from_loc):
                            if neighbor == to_loc:
                                total_distance += distance
                                edge_data.append({
                                    "Từ": from_loc,
                                    "Đến": to_loc,
                                    "Khoảng cách (km)": distance
                                })
                                break
                    
                    
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <div style="font-size: 24px; font-weight: bold; color: #FF4B4B;">Tổng Khoảng cách Mạng lưới: {total_distance} km</div>
                        <div style="font-size: 18px; margin-top: 10px;">Số lượng Kết nối: {len(edge_data)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                  
                    st.subheader("Các Cạnh trong Cây Khung Nhỏ nhất")
                    st.table(pd.DataFrame(edge_data).sort_values("Khoảng cách (km)"))
                    
                    # Hiển thị
                    st.subheader("Cây Khung Nhỏ nhất")
                    
                    # Tạo một đồ thị mới cho MST
                    mst_graph = nx.Graph()
                    
                    # Thêm tất cả các nút
                    for location in travel_graph.vertices:
                        mst_graph.add_node(location)
                    
                    # Thêm các cạnh MST
                    for to_loc, from_loc in mst.items():
                        mst_graph.add_edge(from_loc, to_loc)
                    
                    # Vẽ MST
                    plt.figure(figsize=(15, 10))
                    pos = {loc: coordinates[loc] for loc in mst_graph.nodes() if loc in coordinates}
                    
                    nx.draw_networkx_nodes(mst_graph, pos, node_size=300, node_color='skyblue')
                    nx.draw_networkx_edges(mst_graph, pos, width=2.0, alpha=0.7, edge_color='red')
                    nx.draw_networkx_labels(mst_graph, pos, font_size=8)
                    
                    plt.axis('off')
                    plt.suptitle(f"Cây Khung Nhỏ nhất từ {start_location}\nTổng Khoảng cách: {total_distance} km", fontsize=12)
                    st.pyplot(plt)
                else:
                    st.error(f"Không tìm thấy cây khung nhỏ nhất từ {start_location}")
    
    elif app_mode == "Khám phá Tất cả Địa điểm":
        st.header("Khám phá Tất cả Địa điểm")
        st.write("Xem tất cả các địa điểm có sẵn tại Việt Nam và các kết nối của chúng.")
        
        # Hiển thị tất cả các địa điểm dưới dạng bảng
        st.subheader("Tất cả Địa điểm")
        
        # Tạo một dataframe với thông tin địa điểm
        location_data = []
        for location in locations:
            if location in coordinates:
                neighbors = [neighbor for neighbor, _ in travel_graph.get_neighbors(location)]
                location_data.append({
                    "Địa điểm": location,
                    "Kinh độ": coordinates[location][0],
                    "Vĩ độ": coordinates[location][1],
                    "Kết nối Đến": ", ".join(neighbors),
                    "Số lượng Kết nối": len(neighbors)
                })
        
        df = pd.DataFrame(location_data)
        st.dataframe(df.sort_values("Số lượng Kết nối", ascending=False))
        
        # Hiển thị đồ thị mạng lưới
        st.subheader("Đồ thị Mạng lưới")
        plt = visualize_graph_matplotlib(G)
        plt.suptitle("Tất cả Địa điểm và Kết nối tại Việt Nam", fontsize=12)
        st.pyplot(plt)

    # Thêm footer với tên tác giả
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #e6e6e6;">
    <p>© 2025 Ứng dụng Lập kế hoạch Tuyến đường Du lịch Việt Nam | Phát triển bởi: Duy - Sơn - Thuận</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
