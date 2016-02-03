import java.io.*;
import java.util.*;

class Rating {
    int uid, iid,rating;
    public Rating(int uid, int iid, int r) {
        this.uid = uid;
        this.iid = iid;
        this.rating = r;
    }
}
class Matrix {
    ArrayList<Rating> ratings;
    int rank;
    double[][] P, Q;
    int numUsers, numItems;
    public Matrix(int rank) {
        ratings = new ArrayList<Rating>();
        this.rank = rank;
    }
}

public class NMF {

    Matrix M;
    int numUsers, numItems;
    boolean DEBUG = false;

    public NMF(int k) {
        M = new Matrix(k);
        numUsers = 0;
        numItems = 0;
    }

    public HashMap<Integer, String> loadMovies(String fn) {
        HashMap<Integer, String> map = new HashMap<Integer, String>();
        try {
            BufferedReader br = new BufferedReader(new FileReader(fn));
            String s;
            while((s = br.readLine())!=null) {
                String[] aa = s.split("::");
                int item_id = Integer.parseInt(aa[0]);
                String name = aa[1];
                String genre = aa[2];
                map.put(item_id, name + " " + genre);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return map;
    }

    public void loadMatrixFromMovielens(String fn) {

        try {
            BufferedReader br = new BufferedReader(new FileReader(fn));
            String s;
            while((s = br.readLine())!=null) {
                String[] aa = s.split("::");
                int uid = Integer.parseInt(aa[0]);
                int iid = Integer.parseInt(aa[1]);
                if (numUsers < uid) numUsers = uid;
                if (numItems < iid) numItems = iid;
                int r = Integer.parseInt(aa[2]);
                M.ratings.add(new Rating(uid,iid,r));
            }
            M.numItems = numItems;
            M.numUsers = numUsers;
            M.P = new double[numUsers][M.rank];
            M.Q = new double[numItems][M.rank];
            for(int i = 0; i < numUsers; i++) {
                for (int j = 0; j < M.rank; j++) {
                    M.P[i][j] = 0.1;
                }
            }
            for(int i = 0; i < numItems; i++) {
                for (int j = 0; j < M.rank; j++) {
                    M.Q[i][j] = 0.1;
                }
            }
            System.out.println("#users:" + numUsers + " #items:" + numItems);
            br.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    double innerproduct (double[] a, double[] b) throws Exception {
        int n = a.length;
        if(n!=b.length) throw new Exception("a and b are not of same dimension.");
        double prdt = 0.0;
        for (int i = 0; i < n; i++) {
            prdt += a[i]*b[i];
        }
        return prdt;
    }

    void printArray(double[] a) {
        for (int i = 0; i < a.length; i++) {
            System.out.print(a[i]+" ");
        }
        System.out.println();
    }

    public void sgd(int num_iters)  {
        try {
            double minrmse = Integer.MAX_VALUE;
            double gamma = 0.00005;
            double lambda = 0.0000001;
            for (int iter=0;iter<num_iters;iter++) {
                double rmse = 0.0;
                for (int i = 0; i < M.ratings.size(); i++) {
                    Rating r = M.ratings.get(i);
                    int uid = r.uid;
                    int iid = r.iid;
                    int rating = r.rating;
                    double[] p = M.P[uid - 1];
                    double[] q = M.Q[iid - 1];
                    double predict = innerproduct(p, q);
                    double err = rating - predict;
                    rmse += err * err;
                    for (int j = 0; j < M.rank; j++) {
                        q[j] += (gamma * (2 * p[j] * err - lambda * q[j]));
                        p[j] += (gamma * (2 * q[j] * err - lambda * p[j]));
                    }
                    if (DEBUG&&i % 1000 == 0) {
                        System.out.println("processed " + i + " ratings.");
                    }
                }
                if (DEBUG) {
                    for (int i = 0; i < M.numUsers; i++) {
                        printArray(M.P[i]);
                    }
                    for (int i = 0; i < M.numItems; i++) {
                        printArray(M.Q[i]);
                    }
                }
                if(minrmse>rmse) minrmse = rmse;
                System.out.println(" rmse:" + rmse);
            }
            System.out.println();
            System.out.println("minrmse:"+minrmse/M.ratings.size());
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    public double predict(int user_id, int item_id) {
        try {
            return innerproduct(M.P[user_id], M.Q[item_id]);
        } catch (Exception ex) {
            return 0.0;
        }
    }

    public void loadMatrixFromFile(String fn) {
    }

    public void test(int iters) {
        this.sgd(iters);
    }

    public static void main(String[] args) {
        NMF nmf = new NMF(20);
        nmf.loadMatrixFromMovielens(args[0]);
        HashMap<Integer, String> map_movies = nmf.loadMovies(args[1]);
        System.out.println("loaded");
        nmf.test(Integer.parseInt(args[3]));
        int user_id = Integer.parseInt(args[2]);
        for(int i=0; i<nmf.M.numItems; i++) {
            String movie_name = map_movies.get(i+1);
            System.out.println(movie_name + "\t" + nmf.predict(user_id, i));
        }
    }
}
