import java.io.*;
import java.net.*;
import java.math.BigInteger;

public class Server {
    public static void main(String[] args) {
        // Retry mechanism with time delay
        boolean serverStarted = false;
        int timeDelay = 1000;
        int port = 4000;
        while (!serverStarted) {
            try (ServerSocket serverSocket = new ServerSocket(port)) {
                serverStarted = true;
                InetAddress inetAddress = InetAddress.getLocalHost();
                System.out.println(inetAddress.getHostAddress() + " is listening on port " + port + "...");

                while (true) {
                    try (Socket socket = serverSocket.accept();
                        PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
                        BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

                        String inputLine = input.readLine();
                        String[] parts = inputLine.split(" ");
                        BigInteger compositeNumber = new BigInteger(parts[0]);
                        BigInteger start = new BigInteger(parts[1]);
                        BigInteger stop = new BigInteger(parts[2]);

                        BigInteger factor = findFactor(compositeNumber, start, stop);
                        output.println(factor.toString());
                    } catch (Exception e) {
                        System.out.println("Exception caught when trying to listen on port 4000 or listening for a connection");
                        System.out.println(e.getMessage());
                    }
                }
            } catch (IOException e) {
                System.out.printf("Could not listen on port " + port + ". Retrying in " + timeDelay/1000 + " seconds...");
                System.out.println(e.getMessage());
                try {
                    Thread.sleep(timeDelay);
                    timeDelay *= 2;
                } catch (InterruptedException ex) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    private static BigInteger findFactor(BigInteger number, BigInteger start, BigInteger stop) {

        for (BigInteger i = start; i.compareTo(stop) < 0; i = i.add(BigInteger.ONE)) {
            // System.out.println(i);
            if (number.mod(i).equals(BigInteger.ZERO)) {
                return i;
            }
        }
        return new BigInteger("-1");
    }
}
