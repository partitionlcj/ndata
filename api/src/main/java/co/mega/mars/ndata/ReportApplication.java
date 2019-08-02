package co.mega.mars.ndata;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import redis.clients.jedis.JedisPool;

@ComponentScan(basePackages = {"co.mega.mars"})
@EnableJpaRepositories("co.mega.mars")
@EntityScan("co.mega.mars")
@SpringBootApplication
public class ReportApplication {

	@Bean
	public JedisPool getPool(){
		return new JedisPool("10.25.9.37",13231);
	}

	public static void main(String[] args) {
		SpringApplication.run(ReportApplication.class, args);
	}

}
