package co.mega.mars.ndata;

import co.mega.mars.jwt.JwtConfigurer;
import co.mega.mars.jwt.JwtTokenProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;

@Configuration
public class MarsSecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    JwtTokenProvider jwtTokenProvider;
    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        //@formatter:off
        http
                .httpBasic().disable()
                .csrf().disable()
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                .authorizeRequests()
                .antMatchers(HttpMethod.GET, "/api/auth_token").permitAll()
                .antMatchers(HttpMethod.GET, "/**").hasRole("NDATA_USER")
                .antMatchers(HttpMethod.POST, "/**").hasRole("NDATA_USER")
                //.antMatchers(HttpMethod.GET, "/**").hasRole("REPORT_USER")
                //.antMatchers(HttpMethod.POST, "/**").hasRole("REPORT_USER")
                //.antMatchers(HttpMethod.DELETE, "/**").hasRole("REPORT_USER")
                .and()
                .apply(new JwtConfigurer(jwtTokenProvider));
        //@formatter:on
    }


}
