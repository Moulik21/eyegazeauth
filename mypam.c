#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
 
PAM_EXTERN int pam_sm_setcred( pam_handle_t *pamh, int flags, int argc, const char **argv ) {
	return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv) {
	return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv ) {
	int retval;

	const char* pUsername;

	int waitstatus;
	pid_t pid;
	int ret = 1;
	
	pid = fork();
	// Path may need to be changed depending on who is using it
	char *parms[] = {"/usr/bin/python3", "/lib/security/src/eyegazeauth/User-Interface/login.py", NULL};  
	
	if(pid < 0) {
        	fprintf(stderr, "Fork failed");
        	return 1;
	}

	else if(pid == 0) {

	char uid[1000];
	char gid[1000];
    	FILE *fptr;
    	if ((fptr = fopen("/lib/security/pamuser.txt", "r")) == NULL) {
        	printf("Error! Cannot find PamUser Account!");
       		exit(1);
   	 }

   
   	fscanf(fptr, "%[^\n]", uid);
   	fscanf(fptr, "%[^\n]", gid);
   
    	fclose(fptr);
 	setuid(atoi(uid));
  	setgid(atoi(gid));
  
      	ret = execv(parms[0], parms);
	//We should never get here!
	exit(1);
	}
	else {
		wait(&waitstatus);
		ret = WEXITSTATUS(waitstatus);
	}

	if (ret != 1){
                return PAM_ABORT;
        } else{
                return PAM_SUCCESS;
        }

	return PAM_SUCCESS;
}
