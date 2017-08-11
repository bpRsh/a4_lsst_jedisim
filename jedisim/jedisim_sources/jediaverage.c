/* Author      : Bhishan Poudel
 * Date        : Jul 26, 2016
 * Last update : Sep 17, 2016
 *
 * Inputs      : physics_settings/rescaled_out0.txt
 * Outputs     : average of fitsfiles from input text file
 *
 * Compile     : gcc -O3 -Wall -o jediaverage jediaverage.c -lm -lcfitsio
 *
 * Run         : ./jediaverage physics_settings/rescaled_convolved_lsst_21.txt out1/lsst_0_unnoised.fits
 *
 * Usage       : run_process("jediaverage.c",['./executables/jediaverage',
                    config['output_file'],config['LSST_convolved_image']])
 *
 *               run_process("jediaverage.c",['./executables/jediaverage',
                    config['90_output_file'],config['90_LSST_convolved_image']])
 *
 *
 */


#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#include "fitsio.h"
#define NUM_FILES 21


int main(int argc,char *argv[])
{


char outfile[1024];
strcpy(outfile,argv[2]);

// add ! to the beginning of fitsfile to clobber output fitsfile
//char s[1024];
//strcpy(s,"!");
//strcat(s,l);

// print arguments info
//printf("\ninput textfile: %s:\n",argv[1]);
printf("\nwriting the file     : %s\n", outfile);

// store lines from input text into strings
char fn[NUM_FILES+1][1024];
FILE *fp;
fp = fopen(argv[1],"r");
int n;

for(n=0; n<NUM_FILES; n++){
    fscanf(fp,"%s",fn[n]);
    //printf("%s\n",fn[n]);
}
fclose(fp);

//***************************************************************

fitsfile *in1;
fitsfile *in2;

int ii;        // innermost counter
int status =0;

long naxes[3] = {1,1,1};
int  naxis    = 0;
long npixels  = 1;

long firstpix[3]= {1,1,1};
long bitpix = -32;
double *pix1;
double *pix;

// for averaging
fitsfile *inp;
fitsfile *out;
long   naxes1[3]   = {1,1,1};
int    naxis1      = 0;
double *pixn       = 0;

//open the first fitsfile e.g. aout1.fits
fits_open_file(&in1,fn[1],READONLY,&status);
//create an empty fits file e.g. !trial1/trial1_LSST_convolved.fits
fits_create_file(&in2,outfile,&status);

// check for errors
if(status) {
    fits_report_error(stderr,status);
    return(status);
}

// get dimensions of in1
fits_get_img_dim(in1,&naxis,&status);
fits_get_img_size(in1,3,naxes,&status);

//printf("\nInitial fitsfile values: naxis = %d, naxes[0] = %ld, naxes[1]= %ld\n",naxis, naxes[0], naxes[1]);

// copy header from in1 to in2
fits_copy_header(in1,in2,&status);

// npixels = no of pixels in each row
npixels = naxes[0];

// allocate memory for pix1
pix1 = (double*)malloc(npixels*sizeof(double));

// check for memory allocation error
if(pix1==NULL) {
    printf("memeory allocation error\n");
    return(1);
}


// fill in2 with all zero with same dimesions as in1
//***************************************************************
for(firstpix[2]=1; firstpix[2]<=naxes[2]; firstpix[2]++) {
    for(firstpix[1]=1; firstpix[1]<=naxes[1]; firstpix[1]++) {
        if(fits_read_pix(in1,TDOUBLE,firstpix,npixels,NULL,pix1,NULL,&status))  break;
        for(ii=0; ii<npixels; ii++) {
            pix1[ii] = 0;
        }
        fits_update_key(in2,TLONG,"BITPIX",&bitpix,0,&status);
        fits_write_pix(in2,TDOUBLE,firstpix,npixels,pix1,&status);

    }
}
//*****************************************************************
free(pix1);
fits_close_file(in1,&status);
fits_close_file(in2,&status);


//******************************************************************
for(n=0; n<NUM_FILES; n++) {

    //printf("\n reading file : %s " ,fn[n] );

    fits_open_file(&inp,fn[n],READONLY,&status);
    fits_open_file(&out,outfile,READWRITE,&status);

    pix = (double*)malloc((npixels)*sizeof(double));

    if(status) {
        fits_report_error(stderr,status);
        return status;
    }

    // get dimension and size of input
    fits_get_img_dim(inp,&naxis1,&status);
    fits_get_img_size(inp,3,naxes1,&status);
    npixels = naxes1[0];

    pixn = (double*)malloc((npixels)*sizeof(double));

    for(firstpix[2]=1; firstpix[2]<=naxes1[2]; firstpix[2]++) {
        for(firstpix[1]=1; firstpix[1]<=naxes1[1]; firstpix[1]++) {
            fits_read_pix(inp,TDOUBLE,firstpix,npixels,NULL,pixn,NULL,&status);
            fits_read_pix(out,TDOUBLE,firstpix,npixels,NULL,pix,NULL,&status);

            for(ii=0; ii<npixels; ii++) {
                pix[ii] = ((pix[ii]+pixn[ii])) ;

                if (n==NUM_FILES -1) {
                    //pix[ii] /= 40.0;   // checking
                    pix[ii] /= NUM_FILES;
                }
            }// end loop for ii
            fits_write_pix(out,TDOUBLE,firstpix,npixels,pix,&status);
        } // end lop for firstpix1 is given row, and ii is element in the row
    } // end loop for firstpix2 plane
    fits_close_file(inp,&status);
    free(pixn);
    fits_close_file(out,&status);
    free(pix);
} // end of for loop of 20 files
//******************************************************************


// end of main
printf("\n");
return 0;
}







