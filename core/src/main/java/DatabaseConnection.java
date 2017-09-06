import java.math.BigDecimal;
import java.sql.*;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by dell on 08/08/2017.
 */
public class DatabaseConnection {
    public static void main(String[] args) throws SQLException {
        System.out.println("Gravado");
    }

    public static Connection createConnection() throws SQLException {
        String url = "jdbc:mysql://localhost/extractor";
        String user = "root", passwd = "1234";
        return DriverManager.getConnection(url, user, passwd);
    }

    public void prepareStatement(List<String> datas) {
        Connection connection = null;
        try {
            connection = createConnection();
            String sql = "INSERT INTO extractor.triple (subject_type, subject_value, relation_type, relation_value, object_type, object_value, confidence) VALUES (?,?,?,?,?,?,?)";

            PreparedStatement ps = connection.prepareStatement(sql);

            for (int i = 0; i < datas.size()-1; i++) {
                ps.setString(i+1, datas.get(i));
            }

            ps.setDouble(datas.size(), Double.parseDouble(datas.get(datas.size()-1)));
            ps.execute();
        } catch (SQLException e){
            e.printStackTrace();
        } finally {
            try {
                connection.close();
            } catch (SQLException e1){
                e1.printStackTrace();
            }
        }
    }
}
