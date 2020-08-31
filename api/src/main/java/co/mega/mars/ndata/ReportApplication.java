package co.mega.mars.ndata;

import org.apache.tomcat.util.http.LegacyCookieProcessor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory;
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import redis.clients.jedis.JedisPool;

@ComponentScan(basePackages = {"co.mega.mars"})
@EnableJpaRepositories("co.mega.mars")
@EntityScan("co.mega.mars")
@SpringBootApplication
public class ReportApplication {

	Logger logger = LoggerFactory.getLogger(ReportApplication.class);

	@Value("${ssdb.main.host}")
	String ssdbHost;
	@Value("${ssdb.main.port}")
	int ssdbPort;
	@Value("${ssdb.bcp.host}")
	String ssdbBcpHost;
	@Value("${ssdb.bcp.port}")
	int ssdbBcpPort;

	@Bean("bcpSSDB")
	public JedisPool getBcpPool(){
		return new JedisPool(ssdbBcpHost,ssdbBcpPort);
	}

	@Bean("mainSSDB")
	public JedisPool getMainPool(){
		return new JedisPool(ssdbHost,ssdbPort);
	}

	@Bean
	public WebServerFactoryCustomizer<TomcatServletWebServerFactory> cookieProcessorCustomizer() {
		logger.info("Use LegacyCookieProcessor.");
		return (factory) -> factory.addContextCustomizers(
				(context) -> context.setCookieProcessor(new LegacyCookieProcessor()));
	}

	public static void main(String[] args) {
		SpringApplication.run(ReportApplication.class, args);
	}

}
